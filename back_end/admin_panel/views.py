from rest_framework.views import APIView
from .serializers import  DashboardStatsSerializer, AdminUserSerializer, AdminProductSerializer, AdminCategorySerializer, AdminOrderSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Q
from rest_framework.permissions import IsAdminUser
from accounts.models import Register
from products.models import Product
from orders.models import Order


# ==================== DASHBOARD ====================

class DashboardView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        user_count = Register.objects.filter(is_staff=False).count()
        order_count = Order.objects.count()
        total_revenue = Order.objects.exclude(status='Cancelled').aggregate(
            Sum('total'))['total__sum'] or 0
        
        stats = {
            'user_count': user_count,
            'order_count': order_count,
            'earnings': total_revenue,
            'users': user_count,
            'total_revenue': total_revenue,
        }
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)


# ==================== USER MANAGEMENT ====================

class UserManagementView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, user_id=None):
        try:
            if user_id:
                user = Register.objects.get(id=user_id, is_staff=False)
                serializer = AdminUserSerializer(user)
                return Response(serializer.data)
            
            search = request.query_params.get('search', '')
            users = Register.objects.filter(is_staff=False)
            
            if search:
                users = users.filter(
                    Q(email__icontains=search) |
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search)
                )
            
            users = users.order_by('-date_joined')
            serializer = AdminUserSerializer(users, many=True)
            return Response(serializer.data)
            
        except Register.DoesNotExist:
            return Response({"error": "User not found"}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, user_id):
        try:
            user = Register.objects.get(id=user_id, is_staff=False)
            
            # Update only allowed fields
            if 'restricted' in request.data:
                user.restricted = request.data['restricted']
            if 'is_active' in request.data:
                user.is_active = request.data['is_active']
            
            user.save()
            serializer = AdminUserSerializer(user)
            return Response({
                "message": "User updated successfully",
                "user": serializer.data
            })
            
        except Register.DoesNotExist:
            return Response({"error": "User not found"}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        try:
            user = Register.objects.get(id=user_id, is_staff=False)
            user.delete()
            return Response({"message": "User deleted successfully"})
            
        except Register.DoesNotExist:
            return Response({"error": "User not found"}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== PRODUCT MANAGEMENT ====================

class ProductManagementView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, product_id=None):
        if product_id:
            product = Product.objects.filter(id=product_id).first()
            if not product:
                return Response(
                    {"error": "Product not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(AdminProductSerializer(product).data)

        products = Product.objects.all()

        search = request.query_params.get('search')
        category = request.query_params.get('category')

        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        if category:
            products = products.filter(category_id=category)

        products = products.order_by('-created_at')

        return Response(
            AdminProductSerializer(products, many=True).data
        )

    def post(self, request):
        serializer = AdminProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Product created successfully",
                    "product": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AdminProductSerializer(
            product, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Product updated successfully",
                    "product": serializer.data
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        product.delete()
        return Response({"message": "Product deleted successfully"})

# ==================== ORDER MANAGEMENT ====================

class OrderManagementView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, order_id=None):
        if order_id:
            order = Order.objects.filter(id=order_id).first()
            if not order:
                return Response(
                    {"error": "Order not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(AdminOrderSerializer(order).data)

        orders = Order.objects.all()

        status_filter = request.query_params.get('status')
        search = request.query_params.get('search')

        if status_filter:
            orders = orders.filter(status=status_filter)

        if search:
            orders = orders.filter(
                Q(user__email__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )

        orders = orders.select_related('user') \
                       .prefetch_related('items__product') \
                       .order_by('-placed_at')

        return Response(AdminOrderSerializer(orders, many=True).data)

    def put(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        status_value = request.data.get('status')
        valid_statuses = [
            'Pending', 'Confirmed', 'Shipped',
            'Delivered', 'Cancelled'
        ]

        if status_value not in valid_statuses:
            return Response(
                {"error": f"Status must be one of {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = status_value
        order.save()

        return Response({
            "message": "Order status updated",
            "order": AdminOrderSerializer(order).data
        })
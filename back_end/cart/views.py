from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

# Get user's cart
class GetCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Add item to cart
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response(
                {"error": "product_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Get or create cart
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # If item already exists, increase quantity
            cart_item.quantity += quantity
            cart_item.save()

        # Return updated cart
        cart_serializer = CartSerializer(cart)
        return Response(
            {
                "message": "Item added to cart successfully",
                "cart": cart_serializer.data
            },
            status=status.HTTP_200_OK
        )

# Update cart item quantity
class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        quantity = request.data.get("quantity")

        if quantity is None or quantity < 1:
            return Response(
                {"error": "Quantity must be at least 1"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.quantity = quantity
            cart_item.save()

            cart_serializer = CartSerializer(cart)
            return Response(
                {
                    "message": "Cart item updated successfully",
                    "cart": cart_serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

# Remove item from cart
class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()

            cart_serializer = CartSerializer(cart)
            return Response(
                {
                    "message": "Item removed from cart successfully",
                    "cart": cart_serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

# Clear entire cart
class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            
            cart_serializer = CartSerializer(cart)
            return Response(
                {
                    "message": "Cart cleared successfully",
                    "cart": cart_serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

# Get cart item count
class CartCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            total_count = sum(item.quantity for item in cart.items.all())
            return Response(
                {"count": total_count},
                status=status.HTTP_200_OK
            )
        except Cart.DoesNotExist:
            return Response(
                {"count": 0},
                status=status.HTTP_200_OK
            )
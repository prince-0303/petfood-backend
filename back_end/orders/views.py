from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer

# Create your views here.

class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serialzer = OrderSerializer(data = request.data)

        if serialzer.is_valid():
            serialzer.save(user = request.user)
            return Response(serialzer.data, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = (Order.objects.filter(user = request.user).prefetch_related('items'))
        serailizer = OrderSerializer(order, many = True)
        return Response(serailizer.data)
from django.urls import path
from .views import PlaceOrderView,UserOrderView

urlpatterns = [
    path('placeorder/',PlaceOrderView.as_view()),
    path('orderlist/',UserOrderView.as_view()),
]
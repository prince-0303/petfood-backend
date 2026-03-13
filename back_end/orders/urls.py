from django.urls import path
from .views import PlaceOrderView, UserOrderView, OrderDetailView, AddressListCreateView, AddressDetailView


urlpatterns = [

    path('placeorder/', PlaceOrderView.as_view(), name="placeorder"),
    path('orderlist/', UserOrderView.as_view()),
    path('order/<int:order_id>/', OrderDetailView.as_view()),
    
    path('addresses/', AddressListCreateView.as_view()),
    path('addresses/<int:address_id>/', AddressDetailView.as_view()),
]
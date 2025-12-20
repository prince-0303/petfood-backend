from django.urls import path
from .views import ProductListAPIView, ProductDetailAPIView

urlpatterns = [
    path("list/", ProductListAPIView.as_view()),
    path("list/<int:id>/", ProductDetailAPIView.as_view()),
]
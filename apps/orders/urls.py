from django.urls import path
from .views import OrderCreateView, OrderListView, OrderDetailView, OrderDeleteView

urlpatterns = [
    path("create/", OrderCreateView.as_view()),
    path("", OrderListView.as_view()),
    path("<int:pk>/", OrderDetailView.as_view()),
    path("<int:order_id>/delete/", OrderDeleteView.as_view()),
]
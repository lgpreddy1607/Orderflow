from django.urls import path
from .views import OrderCreateView, OrderListView, OrderDetailView, OrderDeleteView, slow_response

urlpatterns = [
    path("create/", OrderCreateView.as_view()),
    path("", OrderListView.as_view()),
    path("<int:pk>/", OrderDetailView.as_view()),
    path("<int:order_id>/delete/", OrderDeleteView.as_view()),
    path("slow/", slow_response),
]
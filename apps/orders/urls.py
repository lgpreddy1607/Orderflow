from django.urls import path
from .views import OrderCreateView, OrderListView, OrderDetailView, OrderDeleteView
from .views import buffered_test, streaming_test

urlpatterns = [
    path("create/", OrderCreateView.as_view()),
    path("", OrderListView.as_view()),
    path("<int:pk>/", OrderDetailView.as_view()),
    path("<int:order_id>/delete/", OrderDeleteView.as_view()),
    path("buffered-test/", buffered_test),
    path("streaming-test/", streaming_test),
    
]
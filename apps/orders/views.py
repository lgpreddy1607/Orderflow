from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view

import time
import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.models import User

from apps.orders.models import Order
from apps.orders.services import create_order, delete_order

from .serializers import OrderOutputSerializer, OrderCreateSerializer


class OrderCreateView(APIView):

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 🔴 get idempotency key from header
        idempotency_key = request.headers.get("Idempotency-Key")

        user = request.user if request.user.is_authenticated else User.objects.first()

        try:
            order = create_order(
                user=user,
                items=serializer.validated_data["items"],
                idempotency_key=idempotency_key
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"order_id": order.id, "status": order.status},
            status=status.HTTP_201_CREATED
        )


class OrderListView(ListAPIView):
    queryset = Order.objects.prefetch_related("items").all().order_by("-id")
    serializer_class = OrderOutputSerializer

    def list(self, request, *args, **kwargs):
        time.sleep(10)  # simulate slow operation
        return super().list(request, *args, **kwargs)


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderOutputSerializer


class OrderDeleteView(APIView):
    def delete(self, request, order_id):
        delete_order(order_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
     
    
@api_view(["GET"])
def slow_response(request):
    logger.info("START slow_response")
    time.sleep(5)
    logger.info("END slow_response")
    return Response({"status": "done after delay"})
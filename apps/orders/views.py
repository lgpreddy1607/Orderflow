import time
import logging
from django.http import StreamingHttpResponse
from django.db import transaction

logger = logging.getLogger(__name__)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from apps.orders.models import Order
from apps.products.models import Product
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


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderOutputSerializer


class OrderDeleteView(APIView):
    def delete(self, request, order_id):
        delete_order(order_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# =========================
# NGINX BUFFERING TEST ENDPOINTS
# =========================

@api_view(["GET"])
def buffered_test(request):
    return Response({
        "status": "ok",
        "message": "fast response"
    })

@csrf_exempt
def streaming_test(request):
    def generator():
        for i in range(5):
            logger.info(f"Streaming chunk {i}")
            yield f"chunk {i}\n".encode()
            time.sleep(1)

    return StreamingHttpResponse(generator(), content_type="text/plain")


@api_view(["POST"])
def buy_product(request, product_id):
    with transaction.atomic():
        product = Product.objects.select_for_update().get(id=product_id)

        if product.stock > 0:
            time.sleep(5)  # keep this to observe blocking
            product.stock -= 1
            product.save()
            return Response({"status": "success"})
        
        return Response({"status": "out_of_stock"})
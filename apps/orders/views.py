from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView

from django.contrib.auth.models import User

from apps.orders.models import Order
from apps.orders.services import create_order

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
    queryset = Order.objects.all().order_by("-id")
    serializer_class = OrderOutputSerializer


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderOutputSerializer
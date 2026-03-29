from django.db import transaction
from apps.orders.models import Order, OrderItem
from apps.products.models import Product


def create_order(user, items, idempotency_key=None):

    with transaction.atomic():

        # 🔴 Check if already processed
        if idempotency_key:
            existing_order = Order.objects.filter(
                idempotency_key=idempotency_key
            ).first()

            if existing_order:
                return existing_order

        order = Order.objects.create(
            user=user,
            idempotency_key=idempotency_key
        )

        for item in items:
            product = Product.objects.select_for_update().get(id=item["product_id"])

            quantity = item["quantity"]

            if product.stock < quantity:
                raise Exception("Insufficient stock")

            product.stock -= quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchase=product.price
            )

        return order
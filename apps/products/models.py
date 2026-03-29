from django.db import models
from django.db.models import CheckConstraint
from django.db.models import Q

class Product(models.Model):
    name = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=Q(price__gte=0), name="price_gte_0"),
            models.CheckConstraint(condition=Q(stock__gte=0), name="stock_gte_0"),
        ]

    def __str__(self):
        return self.name
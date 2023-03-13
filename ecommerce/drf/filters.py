from django_filters import rest_framework as filters
from ecommerce.inventory.models import Product, ProductInventory

class ProductInventoryFilter(filters.FilterSet):
    price = filters.NumberFilter(field_name="retail_price", lookup_expr="lte")

    class Meta:
        model = ProductInventory
        fields = ["price"]
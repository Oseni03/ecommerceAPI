from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filter
from django.utils.decorators import method_decorator

from ecommerce.inventory.models import Category, Product, ProductInventory

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework import filters

from drf_yasg.utils import swagger_auto_schema


from .serializers import (
    CategorySerializer, ProductSerializer,
    ProductInventorySerializer
)
from .filters import ProductInventoryFilter

# Create your views here.
@method_decorator(
    name='get', decorator=swagger_auto_schema(
        operation_summary="List all category",
        operation_description="This returns all categories"
))
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.prefetch_related("parent").all() 
    serializer_class = CategorySerializer


@method_decorator(
    name='get', decorator=swagger_auto_schema(
        operation_summary="Get single category detail",
        operation_description="This returns a category detail"
))
class CategoryRetrieveView(generics.RetrieveAPIView):
    queryset = Category.objects.prefetch_related("parent").all() 
    serializer_class = CategorySerializer 
    lookup_field = "slug"


class CategoryProductListView(APIView):
    
    @swagger_auto_schema(
        operation_summary="List products by category",
        operation_description="List all products by category slug argument"
    )
    def get(self, request, slug):
        queryset = Product.objects.prefetch_related("category__parent").filter(category__slug=slug)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


@method_decorator(
    name='get', decorator=swagger_auto_schema(
        operation_summary="List product",
        operation_description="This returns all product"
))
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related(
        "category__parent", 
        "inventory__product_type", 
        "inventory__brand",
        "inventory__attribute_values__product_attribute",
        "inventory__stock",
        "inventory__media_product_inventory",
        "inventory__media_product_inventory"
    ).all()
    serializer_class = ProductSerializer 


class ProductRetrieveView(APIView):
    
    @swagger_auto_schema(
        operation_summary="Get single products by web-id",
        operation_description="Get single products by web-id argument"
    )
    def get(self, request, slug=None, web_id=None):
        if slug:
            obj = get_object_or_404(Product, category__slug=slug, web_id=web_id)
        else:
            obj = get_object_or_404(Product, web_id=web_id)
        serializer = ProductSerializer(obj)
        return Response(serializer.data, status.HTTP_200_OK)


@method_decorator(
    name='get', decorator=swagger_auto_schema(
        operation_summary="List inventory",
        operation_description="This returns all inventory"
))
class ProductInventoryListView(generics.ListAPIView):
    queryset = ProductInventory.objects.prefetch_related(
        "product_type", "brand",
        "attribute_values__product_attribute",
        "stock", "media_product_inventory",
    ).filter(is_default=True, is_active=True)
    serializer_class = ProductInventorySerializer 
    filter_backends = [
        filters.SearchFilter, 
        django_filter.DjangoFilterBackend
    ]
    search_fields = [
        "brand__name", "product__name",
        "product_type__name",
        'attribute_values__attribute_value', 
    ]
    ordering_fields = ["price", "title"]
    filterset_class = ProductInventoryFilter


class ProductInventoryRetrieveView(generics.RetrieveAPIView):
    queryset = ProductInventory.objects.prefetch_related(
        "product_type", "brand",
        "attribute_values__product_attribute",
        "stock", "media_product_inventory",
    ).filter(is_default=True, is_active=True)
    serializer_class = ProductInventorySerializer 
    lookup_field = "sku"
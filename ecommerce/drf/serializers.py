from rest_framework import serializers 

from ecommerce.inventory.models import Category, Product, Brand, ProductAttributeValue, Media, ProductInventory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        exclude = ["id"]
        depth = 2
        read_only = True


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand 
        fields = ["name"]


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue 
        depth = 2
        exclude = ["id"]


class MediaSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField(method_name="get_img_url")
    
    class Meta:
        model = Media 
        fields = ["img_url", "alt_text", "is_feature"]
        read_only=True 
    
    def get_img_url(self, obj):
        return obj.img_url.url


class ProductInventorySerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False, read_only=True)
    # product = ProductSerializer(many=False, read_only=True)
    attributes = ProductAttributeValueSerializer(source="attribute_values", read_only=True, many=True)
    images = MediaSerializer(source="media_product_inventory", many=True)
    price = serializers.DecimalField(max_digits=5, decimal_places=2, source="retail_price")
    
    class Meta:
        model = ProductInventory 
        fields = [
            "sku", "product_type", "price",
            "brand", "images", "stock",
            "attributes", "store_price", 
            "sale_price", "is_default"
        ]
        read_only = True 
        # depth = 2


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    inventory = ProductInventorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Product 
        fields = [
            "web_id", "name", 
            "description", "category", 
            "is_active", "inventory"
        ]
        read_only = True
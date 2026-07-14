from rest_framework import serializers
from products.models import Product, Category, Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    gender_label = serializers.CharField(source="get_gender_display", read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "gender", "gender_label", "description")


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "category", "brand", "gender",
            "price", "mrp", "discount_percent", "description",
            "fabric", "color", "rating", "num_ratings", "stock",
            "is_featured", "created_at", "primary_image",
        )

    def get_primary_image(self, obj):
        img = obj.primary_image
        if img and img.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(img.image.url)
            return img.image.url
        return None

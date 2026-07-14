from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from products.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related("category", "brand").all()

    def get_queryset(self):
        qs = super().get_queryset()
        gender = self.request.query_params.get("gender")
        category = self.request.query_params.get("category")
        brand = self.request.query_params.get("brand")
        q = self.request.query_params.get("search")
        if gender:
            qs = qs.filter(gender=gender)
        if category:
            qs = qs.filter(category__slug=category)
        if brand:
            qs = qs.filter(brand__slug=brand)
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(brand__name__icontains=q))
        return qs

    @action(detail=False, methods=["get"])
    def featured(self, request):
        qs = self.get_queryset().filter(is_featured=True)[:12]
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=["get"])
    def genders(self, request):
        from products.models import Gender
        data = {value: label for value, label in Gender.choices}
        return Response(data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True)

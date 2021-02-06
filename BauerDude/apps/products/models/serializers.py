from django.utils.timezone import now
from drizm_django_commons.serializers.super import HrefModelSerializer

from .models import Product
from rest_framework import serializers


class ProductsSerializer(HrefModelSerializer):
    art_nr = serializers.IntegerField()
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = "__all__"
        self_view = "products:products-detail"

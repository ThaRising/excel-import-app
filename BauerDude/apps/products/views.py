from collections import OrderedDict

from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions
from rest_framework.pagination import LimitOffsetPagination as OffsetPag
from rest_framework.response import Response

from .models import Product
from .models import serializers


class LimitOffsetPagination(OffsetPag):
    default_limit = 100
    max_limit = 1000

    def get_paginated_response(self, data):
        response_data = OrderedDict(
            [
                ("count", self.count),
                ("next", self.get_next_link()),
                ("prev", self.get_previous_link()),
                ("results", data),
            ]
        )

        if n := response_data.get("next"):
            response_data["next"] = {"href": n}
        if p := response_data.get("prev"):
            response_data["prev"] = {"href": p}

        return Response(response_data)


class ProductsViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.ProductsSerializer
    queryset = Product.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


def overview_view(request):
    return render(
        request,
        "products/overview.html"
    )

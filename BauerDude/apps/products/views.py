from collections import OrderedDict

from django.http import HttpResponse
from django.template.response import SimpleTemplateResponse
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination as OffsetPag
from rest_framework.response import Response

from .models import Product
from .models.serializers import ProductsSerializer


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


class ProductsView(GenericAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Pagination is still done automatically by DRF because im lazy.
        # Replacing this with an explicit pagination call,
        # may yield pretty high performance gains.
        page = self.paginate_queryset(queryset)

        # Data is rendered by Pydantic and then output raw
        # So we save any overhead from Django and hand the work
        # to orjson's C-bindings.
        serializer = ProductsSerializer(
            count=self.paginator.count,
            next=self.paginator.get_next_link(),
            prev=self.paginator.get_previous_link(),
            results=page
        )
        return HttpResponse(
            serializer.json(),
            content_type="application/json",
            status=200
        )


def overview_view(request):
    return SimpleTemplateResponse("products/overview.html")

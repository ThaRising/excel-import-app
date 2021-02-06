import pandas
from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path, reverse
from drizm_commons.utils.type import IterableKeyDictionary

from . import models


@admin.register(models.Category)
class PriceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    change_list_template = "products/products_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("upload/", self.upload)
        ]
        return custom_urls + urls

    def upload(self, request: HttpRequest):
        excel_file = request.FILES["products"]
        excel = pandas.read_excel(
            excel_file,
            # 0 is 'Kunden', 1 is 'Artikel', 2 is 'Preise'
            sheet_name=[1, 2]
        )
        products, prices = excel[1], excel[2]
        merge: pandas.DataFrame = products.merge(
            prices, how="inner", on="Art.-Nr."
        )
        # Clear memory
        del products
        del prices
        del excel

        # Create Categories
        models.Category.objects.bulk_create(
            [
                models.Category(name=category_name)
                for category_name in merge["Match"].unique()
            ]
        )
        categories = IterableKeyDictionary({
            tuple(
                merge.loc[merge["Match"] == name]["Art.-Nr."]
            ): pk for name, pk in
            list(models.Category.objects.all().values_list("name", "id"))
        })

        # Create Products
        products = []
        for data in merge[merge.columns.difference(["Match"])].values:
            # Structure will be:
            # 0 - art_nr
            # 1 - name
            # 2 - price
            # 3 - weight_units
            # 4 - price_valid_until
            products.append(models.Product(
                art_nr=data[0],
                name=data[1],
                price=data[2],
                weight_units=data[3],
                price_valid_until=data[4]
            ))

        for i, product in enumerate(products):
            product.category_id = categories[product.pk]
            products[i] = product

        models.Product.objects.bulk_create(products)

        # Flash success message
        self.message_user(request, "Upload successful!", messages.SUCCESS)
        return HttpResponseRedirect(
            reverse("admin:products_product_changelist")
        )

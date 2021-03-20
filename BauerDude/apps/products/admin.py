import os
import secrets
import threading

import pandas
from django.contrib import admin, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path, reverse

from . import models


def process_excel_file(filename):
    # Parse the uploaded Excel file to a DataFrame
    with open(filename, "rb") as fin:
        excel = pandas.read_excel(
            fin,
            # 0 is 'Kunden', 1 is 'Artikel', 2 is 'Preise'
            sheet_name=[0, 1, 2]
        )

    customers, products, prices = [excel[i] for i in range(3)]

    # Create all customers, the data structure 'customers' looks like this:
    # kdnr, match, name_short, name, street, zip, city, tel, email
    # The 'Match' and 'name_short' fields are largely identical,
    # so we use the latter and drop the former.
    customers.drop("Match", axis=1, inplace=True)
    customer_fields = (
        "kd_nr", "company_short", "company_name",
        "street", "zip_code", "city", "tel", "email"
    )
    # Map the data from the DataFrame by index to the field names above.
    # The below is basically the same as:
    # for customer in customers: models.Kunde(kd_nr=customer[0], ...)
    models.Kunde.objects.bulk_create([
        models.Kunde(**{k: v for k, v in zip(customer_fields, customer)})
        for customer in customers.values
    ])
    del customers, customer_fields

    # Create the products
    product_fields = ("art_nr", "category", "name", "weight_units")
    models.Product.objects.bulk_create([
        models.Product(**{k: v for k, v in zip(product_fields, product)})
        for product in products.values
    ])
    del product_fields

    # We select only the pk of the product
    # and the 'valid_until' and 'price per weight unit' columns
    prices: pandas.DataFrame = products.merge(
        prices, how="inner", on="Art.-Nr."
    )[["Preis / VPE", "gültig bis", "Art.-Nr."]]
    price_fields = ("value", "valid_until", "parent_id")
    models.Price.objects.bulk_create([
        models.Price(**{k: v for k, v in zip(price_fields, price)})
        for price in prices.values
    ])
    del prices, price_fields, products

    # Delete the user uploaded file
    os.remove(filename)


@admin.register(models.Price)
class PriceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Kunde)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(LoginRequiredMixin, admin.ModelAdmin):
    change_list_template = "products/products_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("upload/", self.upload)
        ]
        return custom_urls + urls

    def upload(self, request: HttpRequest):
        excel_file = request.FILES["products"]
        excel_filename = f"{secrets.token_urlsafe(8)}.xlsx"
        with open(excel_filename, 'wb+') as destination:
            for chunk in excel_file.chunks():  # noqa is file
                destination.write(chunk)

        # Start the main process in the background,
        # so we can give feedback to the user as fast as possible.
        # Note that this should usually be done
        # using Celery worker processes, but this project does not
        # have the necessary Kubernetes infrastructure in place,
        # which would usually be available.
        task = threading.Thread(
            target=process_excel_file,
            args=(excel_filename,),
            daemon=True
        )
        task.start()

        # Flash success message
        self.message_user(request, "Upload successful!", messages.SUCCESS)
        self.message_user(
            request,
            "Your request is being processed, "
            "please allow up to 10 minutes...",
            messages.INFO
        )
        return HttpResponseRedirect(
            reverse("admin:products_product_changelist")
        )

from django.db import models


class Product(models.Model):
    art_nr = models.BigIntegerField(
        primary_key=True, editable=False, verbose_name="Artikel Nr."
    )
    category = models.CharField(max_length=100)
    name = models.TextField()
    weight_units = models.FloatField()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["art_nr"]

    def __str__(self) -> str:
        return str(self.art_nr)


class Price(models.Model):
    value = models.FloatField()
    valid_until = models.DateField()
    parent = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name="prices"
    )

    class Meta:
        verbose_name = "Price"
        verbose_name_plural = "Product Prices"
        ordering = ["parent_id"]

    def __str__(self) -> str:
        return (
            f"Product {self.parent_id} "
            f"({self.parent.name}) - Price {self.value}"
        )


class Kunde(models.Model):
    kd_nr = models.IntegerField(primary_key=True)

    company_name = models.CharField(
        max_length=100,
        help_text=(
            "The companies actual name and legal "
            "entity type, e.g. Wedgetables GmbH."
        )
    )
    company_short = models.CharField(
        max_length=50, help_text=(
            "Descriptive name of the company, e.g. Wedgetables."
        )
    )

    street = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    city = models.CharField(max_length=50)

    tel = models.CharField(
        max_length=25, verbose_name="Telephone Number", unique=True
    )
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Kunde"
        verbose_name_plural = "Kunden"


__all__ = ["Product", "Price", "Kunde"]

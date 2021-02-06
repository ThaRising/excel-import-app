from django.db import models


class Product(models.Model):
    art_nr = models.BigIntegerField(
        primary_key=True, editable=False, verbose_name="Artikel Nr."
    )
    category = models.ForeignKey(
        to="products.Category", on_delete=models.CASCADE, null=True
    )
    price = models.FloatField()
    price_valid_until = models.DateField()
    name = models.TextField()
    weight_units = models.FloatField()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["art_nr"]

    def __str__(self) -> str:
        return str(self.art_nr)


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return str(self.name)


__all__ = ["Product", "Category"]

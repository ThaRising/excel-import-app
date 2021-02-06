from django.contrib import admin
from drizm_django_commons.admin import SortableAdminMenuMixin


class SiteAdmin(SortableAdminMenuMixin, admin.AdminSite):
    site_header = "BauerDude Administration"
    index_title = "BauerDude Administration"
    site_title = "Administration"

    admin_app_ordering = {
        "auth": ("users", "auth"),
        "products": ("products",)
    }

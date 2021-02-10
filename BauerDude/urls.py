from django.contrib import admin
from django.urls import path, include, re_path
from .docs.openapi import schema_view
from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    # Included URL paths
    path('admin/', admin.site.urls),
    # path('djprofile/', include('silk.urls', namespace='silk')),
    # path('djprofile/login/', LoginView.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
    # Note that the browsable API auth is absent,
    # because it uses SessionAuth, while we use JWT
    re_path(r'^favicon\.ico$', favicon_view),

    # JWT Token-Auth endpoints
    path(
        'tokens/',
        include(
            'BauerDude.apps.tokens.urls',
            namespace="tokens"
        )
    ),

    # User defined URL paths
    path(
        'products/',
        include(
            'BauerDude.apps.products.urls',
            namespace="products"
        )
    ),
]

# Add the DebugToolbar only in development mode
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

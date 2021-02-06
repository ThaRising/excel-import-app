from typing import Dict, Tuple, Optional

from django.contrib.auth import get_user_model
from django.http import QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# Default set of credentials for the test user
TEST_USER_EMAIL = "default_tester@tester.de"
TEST_USER_PASSWORD = "shittySecurity420!"


def create_test_user(email: Optional[str] = None,
                     password: Optional[str] = None):
    User = get_user_model()
    user = User.objects.create_user(
        email=email or TEST_USER_EMAIL,
        password=password or TEST_USER_PASSWORD
    )
    return user


def obtain_tokens(cls: APITestCase,
                  credentials: Dict[str, str],
                  query_args: Optional[Dict[str, str]] = None
                  ) -> Tuple[str, str, Response]:
    """ Attempts to obtain a token pair for a set of credentials """
    url = reverse("tokens:obtain_delete")
    if query_args:
        q = QueryDict("", mutable=True)
        q.update(query_args)
        url = "{base_url}?{query_args}".format(
            base_url=url,
            query_args=q.urlencode(),
        )

    res = cls.client.post(url, data=credentials)
    if not res.status_code == status.HTTP_200_OK:
        raise ValueError(
            "Provided testing credentials invalid."
        )

    content = res.json()
    access_token = content.get("access")
    refresh_token = content.get("refresh", None)
    return access_token, refresh_token, res


__all__ = [
    "TEST_USER_EMAIL", "TEST_USER_PASSWORD",
    "create_test_user", "obtain_tokens"
]

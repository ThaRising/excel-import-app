import datetime
from typing import List, Optional, Any

import orjson
from django.db.models import Manager
from pydantic import BaseModel
from pydantic.utils import GetterDict


class ReverseAccessorGetterDict(GetterDict):
    """
    A variant of the default GetterDict, that can correctly
    resolve Djangos Many-to-One reverse-accessors to Lists.
    """
    def get(self, key: Any, default: Any = None) -> Any:
        ret = getattr(self._obj, key, default)
        if isinstance(ret, Manager):
            ret = list(ret.all())
        return ret


class BaseSerializer(BaseModel):
    class Config:
        orm_mode = True
        # We use orjson for maximum serialization performance
        json_loads = orjson.loads
        json_dumps = lambda *a, **kw: orjson.dumps(*a, **kw).decode()


class Price(BaseSerializer):
    value: float
    valid_until: datetime.date


class Product(BaseSerializer):
    art_nr: int
    category: str
    name: str
    weight_units: float
    prices: List[Price]

    class Config:
        getter_dict = ReverseAccessorGetterDict


class ProductsSerializer(BaseSerializer):
    count: int
    next: Optional[str] = None
    prev: Optional[str] = None
    results: Optional[List[Product]] = []

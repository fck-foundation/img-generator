# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class TokenTrendData(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    TokenTrendData - a model defined in OpenAPI

        name: The name of this TokenTrendData [Optional].
        symbol: The symbol of this TokenTrendData [Optional].
        icon_url: The icon_url of this TokenTrendData [Optional].
        price: The price of this TokenTrendData [Optional].
        change: The change of this TokenTrendData [Optional].
    """

    name: Optional[str] = Field(alias="name", default=None)
    symbol: Optional[str] = Field(alias="symbol", default=None)
    icon_url: Optional[AnyUrl] = Field(alias="iconUrl", default=None)
    price: Optional[float] = Field(alias="price", default=None)
    change: Optional[float] = Field(alias="change", default=None)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Scale",
                "symbol": "SCALE",
                "iconUrl": "https://cache.tonapi.io/imgproxy/jHx0m3tMBFj9z9vLy1cooH_v8DIi_2Zi43RLxyfga3g/rs:fill:200:200:1/g:no/aXBmczovL1FtU01pWHNaWU1lZndyVFEzUDZIbkRRYUNwZWNTNEVXTHBnS0s1RVgxRzhpQTg.webp",
                "price": 123.45,
                "change": 2.34,
            },
        }
    }


TokenTrendData.model_rebuild()

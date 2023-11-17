# coding: utf-8

"""
    Token Image Generation API

    API to generate images based on token data.

    The version of the OpenAPI document: 1.0.0
"""


from fastapi import FastAPI

from WidgetGen.apis.token_image_api import router as TokenImageApiRouter

app = FastAPI(
    title="Token Image Generation API",
    description="API to generate images based on token data.",
    version="1.0.0",
)

app.include_router(TokenImageApiRouter)

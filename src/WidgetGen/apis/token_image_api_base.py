# coding: utf-8

from typing import ClassVar, Dict, List, Tuple, IO  # noqa: F401

from WidgetGen.models.token_trend_data import TokenTrendData
from WidgetGen.models.token_vote_data import TokenVoteData


class BaseTokenImageApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseTokenImageApi.subclasses = BaseTokenImageApi.subclasses + (cls,)

    def generate_tokens_trends_image(
        self,
        token_trend_data: List[TokenTrendData],
    ) -> IO[bytes]:
        ...

    def generate_tokens_votes_image(
        self,
        token_vote_data: List[TokenVoteData],
    ) -> IO[bytes]:
        ...

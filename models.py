from pydantic import BaseModel, RootModel
from typing import List


class ASINRecommendation(BaseModel):
    asin: str
    reasoning: str


class ASINRecommendationList(RootModel[List[ASINRecommendation]]):
    pass


class FinalProduct(BaseModel):
    asin: str
    title: str
    price: str
    image: str
    link: str
    reasoning: str

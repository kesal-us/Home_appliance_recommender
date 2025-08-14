from typing import List
from models import ASINRecommendation, FinalProduct, ASINRecommendationList
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0.7)


def query_type(query):
    """Classify if query is about home appliance recommendation."""
    prompt = PromptTemplate.from_template(
        "Is the following query about a home appliance? Reply only with True or False. Query: {query}"
    )
    chain: Runnable = prompt | llm
    result = chain.invoke({"query": query}).content.strip().lower()
    return result == "true"


def recommendation_gen(query, products):
    prompt = PromptTemplate.from_template(
        """You are a home appliance recommendation expert.
            The user is looking for home appliances. From the full list of Amazon products below, pick the top 3 most suitable products. For each one, return:
            - asin
            - reasoning (why you selected it for the user)
            Respond in this exact format:
            [{{"asin": "...", "reasoning": "..."}}, ...]

            User Query:
            {query}

            Product List:
            {products}
            """
    )

    parser = PydanticOutputParser(pydantic_object=ASINRecommendationList)
    chain = prompt | llm | parser
    result = chain.invoke({"query": query, "products": products})
    return result.root



def formater_output(recommendations,products):
    asin_to_product = {p["asin"]: p for p in products}
    formated = []

    for rec in recommendations:
        prod = asin_to_product.get(rec.asin)
        if prod:
            formated.append(FinalProduct(
                asin=rec.asin,
                title=prod["product_title"],
                price=prod["product_price"],
                image=prod["product_photo"],
                link=prod["product_url"],
                reasoning=rec.reasoning
            ))

    return formated

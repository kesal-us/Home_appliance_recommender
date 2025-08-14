from langgraph.graph import StateGraph, END, START
from typing import TypedDict, List
from models import ASINRecommendation, FinalProduct
from scraper import search_amazon
from utils import query_type, recommendation_gen, formater_output


class RecommenderState(TypedDict):
    user_query: str
    products: list
    relevant: bool
    recommendation: List[ASINRecommendation]
    response: List[FinalProduct]


def classify(state: RecommenderState) -> RecommenderState:
    relevant = query_type(state["user_query"])
    return {**state, "relevant": relevant}


def scrape(state: RecommenderState) -> RecommenderState:
    products = search_amazon(state["user_query"])
    return {**state, "products": products}


def recommend(state: RecommenderState) -> RecommenderState:
    recommendations = recommendation_gen(state["user_query"], state["products"])
    print(recommendations)
    return {**state, "recommendation": recommendations}


def format(state: RecommenderState) -> RecommenderState:
    final = formater_output(state["recommendation"], state["products"])
    print(final)
    return {**state, "response": final}


def router(state: RecommenderState) -> str:
    return "scrape" if state["relevant"] else END


def build_graph():
    graph = StateGraph(RecommenderState)

    graph.add_node("classify", classify)
    graph.add_node("scrape", scrape)
    graph.add_node("recommend", recommend)
    graph.add_node("format_output", format)

    # Router node (acts like a conditional redirector)
    graph.set_entry_point("classify")

    # classify → router decision (replaces old conditional edge)
    graph.add_conditional_edges("classify", router,{"scrape":"scrape",END:END})

    # Linear steps if relevant
    graph.add_edge("scrape", "recommend")
    graph.add_edge("recommend", "format_output")
    graph.add_edge("format_output", END)

    return graph.compile()

# app=build_graph()
# from IPython.display import Image

# Image(app.get_graph().draw_mermaid_png())

# with open("graph.png", "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())
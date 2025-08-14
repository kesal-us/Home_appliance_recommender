import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "real-time-amazon-data.p.rapidapi.com"


def search_amazon(query: str) -> list:
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    params = {"query": query,"country": "IN","page": "1"}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("products", [])
    except Exception as e:
        print(f"Error fetching Amazon data: {e}")
        return []

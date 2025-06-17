import cohere
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("COHERE_API_KEY")
client = cohere.ClientV2(API_KEY)


def response_config(history: list):
    response = client.chat(
        model="command-a-03-2025",
        messages=history,
        temperature=0.3,
        stop_sequences=["User:", "RentaBot:"],
        frequency_penalty=0.3,
    )
    return response

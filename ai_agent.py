from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
import requests

import os
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant"
)

def process_input(state):
    user_input = state["input"]

    prompt = f"""
Extract the following fields from text and return ONLY valid JSON.

doctor_name:
date:
notes:
followup:

Text:
{user_input}
"""

    response = llm.invoke(prompt)

    state["structured"] = response.content
    return state

import json
def save_backend(state):
    try:
        data = json.loads(state["structured"])
    except:
        print("JSON parsing error")
        print(state["structured"])
        return state

    requests.post(
        "http://127.0.0.1:8000/add",
        json=data
    )

    return state

    requests.post(
        "http://127.0.0.1:8000/add",
        json=data
    )

    return state


workflow = StateGraph(dict)

workflow.add_node("process", process_input)
workflow.add_node("save", save_backend)

workflow.set_entry_point("process")
workflow.add_edge("process", "save")
workflow.add_edge("save", END)

app = workflow.compile()


if __name__ == "__main__":
    text = input("Enter interaction: ")
    app.invoke({"input": text})
import json
from openai import OpenAI
import os

from app.tools import TOOLS, retrieve_tool
from app import rag

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def run_agent(user_query: str) -> str:
    """
    Simple agent:
    1. Model decides if it needs retrieval
    2. If model outputs a function call -> run the tool
    3. Send tool output back to model
    4. Return final answer
    """

    # Step 1: ask model what to do
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI agent that decides whether to use tools. "
                    "If the question requires document context, call retrieve_tool. "
                    "Otherwise, answer directly."
                )
            },
            {"role": "user", "content": user_query}
        ],
        functions=TOOLS,
        function_call="auto"
    )

    msg = response.choices[0].message

    # Step 2: If model decided to call a tool
    if msg.function_call:
        func = msg.function_call
        name = func.name
        args = json.loads(func.arguments)

        if name == "retrieve_tool":
            tool_output = retrieve_tool(**args)

            # Step 3: Send tool output back to the model
            second = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an assistant that answers using retrieved chunks. "
                            "Use ONLY the provided retrieved context."
                        ),
                    },
                    {"role": "user", "content": user_query},
                    {
                        "role": "function",
                        "name": "retrieve_tool",
                        "content": json.dumps(tool_output)
                    }
                ]
            )

            return second.choices[0].message.content.strip()

    # Step 4: If no tool was used → direct answer
    return msg.content.strip()

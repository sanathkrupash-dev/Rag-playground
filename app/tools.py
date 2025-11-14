"""
Tool definitions for the RAG Agent.
These tools can be called by the agent using OpenAI function calling.
"""

from typing import List, Dict
from app import rag


def retrieve_tool(query: str, k: int = 3) -> Dict:
    """
    Tool: Retrieve top-k chunks from the vector DB.
    Returns chunk text + scores.
    """
    chunks = rag.retrieve(query, k=k)
    return {
        "query": query,
        "k": k,
        "chunks": chunks
    }


TOOLS = [
    {
        "name": "retrieve_tool",
        "description": "Retrieve relevant document chunks for a query from the RAG vector store.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "k": {"type": "integer", "default": 3},
            },
            "required": ["query"]
        },
    }
]

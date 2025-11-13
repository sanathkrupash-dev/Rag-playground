"""
Entry point for Snowflake RAG Playground.

For now, this just:
- asks the user for a question in the terminal
- calls the placeholder RAG `answer` function
- prints the response

In Week 2 we'll wire this to the real RAG pipeline.
"""
from . import rag


def main():
    print("=== Snowflake RAG Playground ===")
    query = input("Ask a question about the Snowflake platform (or 'exit'): ").strip()

    if not query or query.lower() == "exit":
        print("Exiting.")
        return

    response = rag.answer(query)
    print("\n--- Answer ---")
    print(response)
    print("--------------")


if __name__ == "__main__":
    main()

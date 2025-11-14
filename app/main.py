from . import rag


def main():
    print("=== Snowflake RAG Playground ===")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Ask a question about the Snowflake platform: ").strip()

        if not query or query.lower() == "exit":
            print("Goodbye 👋")
            break

        response = rag.answer(query)
        print("\n--- Answer ---")
        print(response)
        print("--------------\n")


if __name__ == "__main__":
    main()

import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


DB_DIR = "db"


def load_vector_db(collection_name):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db_path = os.path.join(DB_DIR, collection_name)

    vectorstore = FAISS.load_local(
        db_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def search_collection(collection_name, query, k=3):
    print(f"\nSearching in: {collection_name}")
    print(f"Query: {query}")
    print("-" * 60)

    vectorstore = load_vector_db(collection_name)
    results = vectorstore.similarity_search(query, k=k)

    for i, doc in enumerate(results, start=1):
        print(f"\nResult {i}")
        print(doc.page_content)
        print(f"Source: {doc.metadata.get('source')}")
        print("-" * 60)


if __name__ == "__main__":

    while True:
        print("\nCareer&Skills AI - RAG Retrieval Test")
        print("1. Search Jobs")
        print("2. Search Courses")
        print("3. Search Resume Samples")
        print("4. Search Policy")
        print("5. Exit")

        choice = input("\nChoose option: ")

        if choice == "5":
            print("Exiting test.")
            break

        query = input("Enter your search query: ")

        if choice == "1":
            search_collection("jobs", query)
        elif choice == "2":
            search_collection("courses", query)
        elif choice == "3":
            search_collection("resume_samples", query)
        elif choice == "4":
            search_collection("policy", query)
        else:
            print("Invalid choice. Please try again.")
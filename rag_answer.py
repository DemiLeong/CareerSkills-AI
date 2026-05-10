import os
from dotenv import load_dotenv
from groq import Groq

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

DB_DIR = "db"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def load_vector_db(collection_name):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db_path = os.path.join(DB_DIR, collection_name)

    return FAISS.load_local(
        db_path,
        embeddings,
        allow_dangerous_deserialization=True
    )


def retrieve_context(collection_name, query, k=3):
    vectorstore = load_vector_db(collection_name)
    docs = vectorstore.similarity_search(query, k=k)

    context = "\n\n".join([doc.page_content for doc in docs])
    return context


def generate_answer(collection_name, query):
    context = retrieve_context(collection_name, query)

    prompt = f"""
You are PathFinder AI, a helpful career navigation assistant.

Use the context below to answer the user's question.
Do not invent information outside the context.
If the answer is not found, say you do not have enough information.

Context:
{context}

User Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("\nPathFinder AI - RAG Answer Test")
    print("1. Jobs")
    print("2. Courses")
    print("3. Resume Samples")
    print("4. Policy")

    choice = input("\nChoose collection: ")
    query = input("Enter your question: ")

    if choice == "1":
        collection = "jobs"
    elif choice == "2":
        collection = "courses"
    elif choice == "3":
        collection = "resume_samples"
    elif choice == "4":
        collection = "policy"
    else:
        print("Invalid choice.")
        exit()

    answer = generate_answer(collection, query)

    print("\nPathFinder AI Answer:")
    print("-" * 60)
    print(answer)
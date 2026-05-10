import os
from dotenv import load_dotenv
from groq import Groq

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_DIR = os.path.join(BASE_DIR, "db")


def load_policy_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.load_local(
        os.path.join(DB_DIR, "policy"),
        embeddings,
        allow_dangerous_deserialization=True
    )


def retrieve_policy(query, k=3):
    vectorstore = load_policy_db()
    docs = vectorstore.similarity_search(query, k=k)

    return "\n\n".join([doc.page_content for doc in docs])


def policy_agent(user_query):
    policy_context = retrieve_policy(user_query)

    prompt = f"""
You are Career&Skills AI's Policy Agent.

Your task:
1. Answer policy, privacy, ethics, or usage questions.
2. Explain what users should and should not upload.
3. Remind users not to share sensitive personal data.
4. Keep the answer clear and beginner-friendly.

Important:
- Use only the policy context provided.
- Do not create legal claims.
- This is an educational AI system, not legal advice.

User Question:
{user_query}

Policy Context:
{policy_context}

Return your answer in this format:

## Policy Answer
## What Users Should Avoid Uploading
## Safe Usage Advice
## Important Reminder
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    sample_query = "What personal information should I avoid uploading?"

    result = policy_agent(sample_query)

    print("\nCareer&Skills AI - Policy Agent Test")
    print("-" * 60)
    print(result)
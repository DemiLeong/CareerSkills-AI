import os
from dotenv import load_dotenv
from groq import Groq

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_DIR = os.path.join(BASE_DIR, "db")


def load_jobs_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.load_local(
        os.path.join(DB_DIR, "jobs"),
        embeddings,
        allow_dangerous_deserialization=True
    )


def retrieve_jobs(query, k=5):
    vectorstore = load_jobs_db()
    docs = vectorstore.similarity_search(query, k=k)

    return "\n\n".join([doc.page_content for doc in docs])


def information_agent(user_query, resume_text=""):
    search_query = f"""
    User Query:
    {user_query}

    Resume:
    {resume_text}
    """

    job_context = retrieve_jobs(search_query)

    prompt = f"""
        You are a professional AI Career Advisor.

        Your role is to:
        - analyze the user's resume, skills, and experience
        - recommend suitable job roles
        - explain why the jobs are suitable
        - identify missing skills
        - suggest career progression pathways
        - suggest industries that match the user's background

        DO NOT rewrite the user's resume.
        DO NOT generate resume formatting.

        Focus on career recommendations and job suitability only.

        Important:
        - Use only the job context provided.
        - Do not invent companies or job roles.
        - If the information is not available, say so clearly.

        Formatting rules:
        - Use markdown headings with ##.
        - Use bullet points for lists.
        - Do not return HTML tags such as <p>, <br>, or <ul>.
        - Keep sections readable with short paragraphs.

        Retrieved Job Context:
        {job_context}

        User Resume:
        {resume_text}

        User Question:
        {user_query}
        

    Return your answer in this format:

    ## Career / Job Information
    ## Relevant Job Roles
    ## Skills Commonly Required
    ## Possible Skill Gaps
    ## Practical Advice
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
    sample_query = "What jobs are suitable for someone with Python, SQL, and Excel?"

    sample_resume = """
Skills: Python, SQL, Excel
Experience: Junior analyst doing reports and dashboards.
"""

    result = information_agent(sample_query, sample_resume)

    print("\nCareer&Skills AI - Information Agent Test")
    print("-" * 60)
    print(result)
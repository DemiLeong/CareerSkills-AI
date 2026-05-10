import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def interview_agent(target_role, user_background, interview_type, job_description=""):
    prompt = f"""
    You are Career&Skills AI's Interview Preparation Agent.

    Your task:
    1. Generate interview questions for the target role.
    2  Tailor questions to the job description provided in the Your Interview Request field,if any.
    3. Provide suggested answer guidance.
    4. Include technical and behavioural questions.
    5. Give preparation tips.

    Important:
    - Keep answers beginner-friendly.
    - Do not invent the user's experience.
    - Tailor advice to the user's background if provided.
    - Do not create a ticket number.
    - Do NOT simulate human escalation.
    - If human support is needed, advise the user to go to the Human Escalation service and submit the form with name, email, and request details.

    Formatting rules:
    - Use markdown headings with ##.
    - Use bullet points and numbered questions.
    - Do not return HTML tags such as <p>, <br>, or <ul>.
    - Keep each answer suggestion short and readable.

    Target Role:
    {target_role}

    User Background:
    {user_background}

    Interview Type:
    {interview_type}

    Return your answer in this format:

    ## Interview Preparation Overview
    ## Technical Questions
    ## Behavioural Questions
    ## Suggested Answer Guidance
    ## Preparation Tips
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    sample_role = "Data Analyst"

    sample_background = """
Skills: Python, SQL, Excel
Experience: Junior analyst doing reports and dashboards.
"""

    result = interview_agent(
        target_role=sample_role,
        user_background=sample_background,
        interview_type="technical and behavioural"
    )

    print("\nCareer&Skills AI - Interview Agent Test")
    print("-" * 60)
    print(result)
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from groq import Groq
from duckduckgo_search import DDGS


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def web_search_courses(target_role, career_goal, max_results=10):
    search_query = f"""
    site:myskillsfuture.gov.sg SkillsFuture Singapore course
    {target_role}
    {career_goal}
    """

    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(
            search_query,
            region="sg-en",
            safesearch="moderate",
            max_results=max_results
        ):
            results.append({
                "title": r.get("title", ""),
                "snippet": r.get("body", "")
            })

    return results


def format_search_context(results):
    context = ""

    for i, result in enumerate(results, start=1):
        context += f"""
Search Result {i}
Title: {result["title"]}
Snippet: {result["snippet"]}
"""

    return context


def course_agent(resume_text, target_role, career_goal):
    search_results = web_search_courses(
        target_role=target_role,
        career_goal=career_goal
    )

    search_context = format_search_context(search_results)

    prompt = f"""
    You are Career&Skills AI's Course Recommendation Agent.

    Your role is to help users identify relevant learning directions, skill areas, and SkillsFuture search keywords.

    IMPORTANT RULES:
    - Do NOT invent or hallucinate course names.
    - Do NOT write any specific course title unless it appears word-for-word in the provided search context.
    - If uncertain whether a course exists, do NOT generate a course title.
    - Instead of course names, recommend:
    - learning topics
    - skill areas
    - certification areas
    - SkillsFuture search keywords
    - Search keywords should be short and practical.
    - Prioritize Singapore-relevant upskilling recommendations.
    - Encourage users to verify latest course availability on MySkillsFuture.

    User Resume / Skills Summary:
    {resume_text}

    Target Role:
    {target_role}

    Career Goal:
    {career_goal}

    Provided Search Context:
    {search_context}

    Return your answer in this format:

    ## Career Goal Understanding
    Briefly explain the user's career goal.

    ## Current Skill Summary
    Summarize the user's current skills based only on the resume or skill summary provided.

    ## Recommended Learning Topics
    Recommend learning topics only. Do NOT write course names.

    For each recommended learning topic, use this exact format:

    ### Topic: <topic name>

    #### Why it is useful:
    <short explanation>

    #### SkillsFuture Search Keyword To Use:
    <keyword>

    ## Recommended Skill Areas
    List important skill areas to develop using short bullet points.

    ## Suggested Learning Path
    Give a simple beginner-to-intermediate learning path.

    ## Verification Reminder
    Remind the user to verify latest course availability, fees, subsidies, eligibility, and intake dates directly on MySkillsFuture.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    sample_resume = """
    Skills: communication, facilitation, Excel, operations coordination.
    Experience: Training coordinator supporting workshops and learner administration.
    """

    result = course_agent(
        resume_text=sample_resume,
        target_role="WSQ Trainer",
        career_goal="I want to become a WSQ Trainer or adult educator."
    )

    print(result)
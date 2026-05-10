import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def resume_agent(resume_text, job_title, job_description):
    prompt = f"""
    You are Career&Skills AI's Resume Rewrite Agent.

    Your purpose is to rewrite the user's resume to improve clarity, professionalism, ATS-readability, and alignment with the job application.

    CRITICAL RULES:
    1. Do NOT invent experience.
    2. Do NOT add skills that are missing from the user's resume.
    3. Do NOT move missing skills into the final resume draft.
    4. Only use skills, tools, education, projects, and experience that appear in the user's resume.
    5. You may improve wording, grammar, structure, and professional tone.
    6. You may highlight transferable skills already shown in the resume.
    7. You may use keywords from the job description ONLY if they are supported by the resume.
    8. If a required skill is missing, list it separately under "Missing Skills", but do NOT include it in the rewritten resume.
    9. The final output should help the resume pass initial ATS/AI screening without being dishonest.

    Job Title Applied:
    {job_title}

    Job Description:
    {job_description}

    User Resume:
    {resume_text}

    Return your answer in this format:

    ## Resume Match Summary
    Briefly explain how well the resume matches the job.

    ## Existing Skills Found in Resume
    List only skills that are clearly found in the user's resume.

    ## Missing Skills From Job Description
    List skills required by the job but NOT found in the resume.
    Add this note: "Do not add these to your resume unless you genuinely have these skills."

    ## ATS-Friendly Keywords You Can Safely Use
    List keywords from the job description that are supported by the user's resume.

    ## Rewritten Resume Summary
    Rewrite a stronger professional summary for the job title applied.
    Use only true information from the resume.

    ## Rewritten Key Skills Section
    Rewrite the key skills section using only skills found in the resume.

    ## Rewritten Work Experience
    Format this section as bullet points.
    Each work experience should have:
    - Job title / role if available
    - Company if available
    - 3 to 8 rewritten bullet points
    Do not write this as one big paragraph. 
    Use line breaks between different work experiences.
    Bold the company name and work duration in each work experience.
    In each work experience, use line breaks between bullet points. Do not write everything in one paragraph.
    line breaks between sections.
    

    ## Final Tailored Resume Draft
    Format this like a readable resume with clear sections:
    - Professional Summary
    - Key Skills
    - Work Experience
    - Education
    - Projects / Certifications if available

    Use bullet points for skills and work experience.
    Use line breaks between sections.
    Bold the company name and work duration in each work experience.
    In each work experience, start a new line for each bullet point (-). Do not write this as one big paragraph. 
    Do not bold the content of the Education section, but use line breaks between different education entries.
    Do not bold the content of the Projects / Certifications section, but use line breaks between different entries.
    Do not write everything in one paragraph.
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content
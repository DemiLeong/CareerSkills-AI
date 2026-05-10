import os
import sys
import re
import markdown

from urllib.parse import quote_plus
from typing import cast
from datetime import datetime
from textwrap import dedent

from flask import (
    Flask,
    render_template,
    request
)

from docx import Document
from pypdf import PdfReader


# -------------------------------------------------
# ROOT PATH SETUP
# -------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

ROOT_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..")
)

sys.path.insert(0, ROOT_DIR)


# -------------------------------------------------
# SHARED BACKEND IMPORTS
# -------------------------------------------------

from langgraph_app import careerskills_app, CareerSkillsState
from utils.email_helper import send_acknowledgement_email


# -------------------------------------------------
# FLASK APP
# -------------------------------------------------

app = Flask(__name__)


# -------------------------------------------------
# HELPERS
# -------------------------------------------------

def read_uploaded_resume(file):

    if not file or file.filename == "":
        return ""
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        return file.read().decode("utf-8")
    
    if filename.endswith(".docx"):
        doc = Document(file)
        return "\n".join(
            [p.text for p in doc.paragraphs]
        )

    if filename.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    return ""


def add_course_search_links(ai_response):

    pattern = r'(?:SkillsFuture Search Keyword To Use):\s*([^\n<]+)'

    def replace_match(match):

        keyword = match.group(1).strip()

        url = (
            "https://courses.myskillsfuture.gov.sg/search?q="
            + quote_plus(keyword)
            + "&page=1&hasUpcomingCourseRun=false"
        )

        # return (
        #    f"SkillsFuture Search Keyword To Use: "
        #    f"**{keyword}**\n\n"
        #     f"[Open MySkillsFuture Search]({url})"

        return (
            f"SkillsFuture Search Keyword To Use: "
            f"**{keyword}**\n\n"
            f'<a href="{url}" '
            f'target="_blank" '
            f'rel="noopener noreferrer">'
            f'Open MySkillsFuture Search'
            f'</a>'
        )

    return re.sub(
        pattern,
        replace_match,
        ai_response
    )


def format_ai_response(ai_response):
    clean_text = dedent(ai_response).strip()

    html = markdown.markdown(
        clean_text,
        extensions=["extra"]
    )

    return html

# -------------------------------------------------
# HOME
# -------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# -------------------------------------------------
# RESUME REWRITE
# -------------------------------------------------

@app.route("/resume", methods=["GET", "POST"])
def resume():

    ai_response = None

    if request.method == "POST":

        instruction = request.form.get("instruction", "")
        resume_text = request.form.get("resume_text", "")

        resume_file_text = read_uploaded_resume(
            request.files.get("resume_file")
        )

        if resume_file_text:
            resume_text = resume_file_text

        job_title = request.form.get("job_title", "")
        job_description = request.form.get("job_description", "")

        state = {
            "query": "resume rewrite: " + instruction,
            "resume_text": resume_text,
            "job_description": job_description,
            "job_title": job_title,
            "target_role": "",
            "career_goal": "",
            "resume_mode": "advice",
            "next_node": "",
            "response": ""
        }

        result = careerskills_app.invoke(
            cast(CareerSkillsState, state)
        )

        ai_response = format_ai_response(result["response"])

    return render_template(
        "resume.html",
        ai_response=ai_response
    )


# -------------------------------------------------
# COURSE RECOMMENDATION
# -------------------------------------------------

@app.route("/courses", methods=["GET", "POST"])
def courses():

    ai_response = None

    if request.method == "POST":
        resume_text = request.form.get(
            "resume_text",
            ""
        )
        target_role = request.form.get(
            "target_role",
            ""
        )

        career_goal = request.form.get(
            "career_goal",
            ""
        )

        state = {
            "query": (
                "course recommendation and "
                "upskilling advice"
            ),
            "resume_text": resume_text,
            "job_description": "",
            "job_title": "",
            "target_role": target_role,
            "career_goal": career_goal,
            "resume_mode": "",
            "next_node": "",
            "response": ""
        }

        result = careerskills_app.invoke(
            cast(CareerSkillsState, state)
        )

        ai_response = format_ai_response(result["response"])

        # Add clickable SkillsFuture links
        ai_response = add_course_search_links(
            result["response"]
        )

        # Convert markdown to professional HTML
        ai_response = format_ai_response(
            ai_response
        )

    return render_template(
        "courses.html",
        ai_response=ai_response
    )


# -------------------------------------------------
# CAREER / JOB ADVICE
# -------------------------------------------------

@app.route("/career", methods=["GET", "POST"])
def career():

    ai_response = None

    if request.method == "POST":

        query = request.form.get(
            "query",
            ""
        )

        resume_text = request.form.get(
            "resume_text",
            ""
        )

        state = {
            "query": (
                "career recommendation and "
                "job matching advice: "
                + query
            ),
            "resume_text": resume_text,
            "job_description": "",
            "job_title": "",
            "target_role": "",
            "career_goal": "",
            "resume_mode": "",
            "next_node": "",
            "response": ""
        }

        result = careerskills_app.invoke(
            cast(CareerSkillsState, state)
        )

        ai_response = format_ai_response(
            result["response"]
        )

    return render_template(
        "career.html",
        ai_response=ai_response
    )


# -------------------------------------------------
# INTERVIEW PREPARATION
# -------------------------------------------------

@app.route("/interview", methods=["GET", "POST"])
def interview():

    ai_response = None

    if request.method == "POST":

        query = request.form.get(
            "query",
            ""
        )

        job_description = request.form.get(
            "job_description", 
            ""
        )

        target_role = request.form.get(
            "target_role",
            ""
        )

        resume_text = request.form.get(
            "resume_text",
            ""
        )

        state = {
            "query": (
                "interview preparation: "
                + query
            ),
            "resume_text": resume_text,
            "job_description": "",
            "job_title": "",
            "target_role": target_role,
            "career_goal": "",
            "resume_mode": "",
            "next_node": "",
            "response": ""
        }

        state = {
            "query": "interview preparation: " + query,
            "resume_text": resume_text,
            "job_description": job_description,
            "job_title": "",
            "target_role": target_role,
            "career_goal": "",
            "resume_mode": "",
            "next_node": "",
            "response": ""
        }


        result = careerskills_app.invoke(
            cast(CareerSkillsState, state)
        )

        ai_response = format_ai_response(
            result["response"]
        )

    return render_template(
        "interview.html",
        ai_response=ai_response
    )


# -------------------------------------------------
# POLICY & PRIVACY
# -------------------------------------------------

@app.route("/policy")
def policy():

    return render_template(
        "policy.html"
    )


# -------------------------------------------------
# HUMAN ESCALATION
# -------------------------------------------------

@app.route("/human", methods=["GET", "POST"])
def human():

    success_message = None
    error_message = None

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        )

        first_name = request.form.get(
            "first_name",
            ""
        )

        last_name = request.form.get(
            "last_name",
            ""
        )

        email = request.form.get(
            "email",
            ""
        )

        years_experience = request.form.get(
            "years_experience",
            ""
        )

        request_description = request.form.get(
            "request_description",
            ""
        )

        ticket_id = (
            "CSAI-"
            + datetime.now().strftime("%Y%m%d%H%M%S")
        )

        success, message = (
            send_acknowledgement_email(
                to_email=email,
                ticket_id=ticket_id,
                title=title,
                first_name=first_name,
                request_description=request_description
            )
        )

        if success:

            success_message = format_ai_response(
                f"""
                ## Request Submitted Successfully
                Your request has been received successfully.

                ### Ticket Number: {ticket_id}
                An acknowledgement email has been sent to your email address.
                """
            )

        else:

            error_message = format_ai_response(
                f"""
                ## Email Delivery Failed
                Your ticket was created successfully.

                ### Ticket Number
                **{ticket_id}**
                However, the acknowledgement email could not be sent.

                ### Error Details
                {message}
                """
            )

    return render_template(
        "human.html",
        success_message=success_message,
        error_message=error_message
    )


# -------------------------------------------------
# RUN APP
# -------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)
# 🚀 Career&Skills AI  
## Online Support Agent Capstone Project  
### AI-Powered Career, Resume, Course, Interview & Human Escalation Assistant

---

## 👤 Author Information

| Item | Details |
|---|---|
| **Learner Name** | Leong Sow Quen |
| **Institution** | National Technological University (NTU) |
| **Course** | SCTP Advanced Professional Certificate in Data Science and AI, FT2 |
| **Project Title** | Online Support Agent Capstone Project |
| **System Name** | Career&Skills AI |
| **Tagline** | Navigate Your Future |

---

## 🌟 Project Introduction

**Career&Skills AI** is an AI-powered online career support agent developed as a capstone project.  
The system is designed to help users with career development, resume improvement, upskilling recommendations, interview preparation, and human escalation support.

The project demonstrates how **Generative AI, RAG, LangGraph, Flask, Streamlit, Groq, FAISS, DuckDuckGo Search, and email automation** can be combined into a practical AI support system.

---

## 🎓 Training Purpose: Two Versions Created

This project includes **two application versions** for learning and comparison purposes.

| Version | Purpose | Main Use |
|---|---|---|
| **Streamlit Version** | Rapid AI prototyping and testing | Easier for beginners to build and debug |
| **Flask Web Version** | Professional web application structure | Better for learning HTML, CSS, JavaScript, routing, forms, and backend integration |

### Why Two Versions?

The two versions were created intentionally for training purposes:

1. **Streamlit Version**
   - Easier to build quickly
   - Good for testing AI agents
   - Useful for rapid prototyping
   - Beginner-friendly interface

2. **Flask Web Version**
   - More professional web structure
   - Uses HTML/CSS/JS frontend
   - Better for understanding real web development
   - Allows custom UI design and service pages

Both versions share the **same AI backend**, including:
- `app.py`
- `agents/`
- `utils/`
- `db/`
- RAG vector database
- LangGraph workflow

This means both frontends use the same AI logic.

---

## 🧠 What The System Can Do

Career&Skills AI provides the following services:

### 📄 1. Resume Rewrite Agent
Helps users rewrite and improve resumes for a selected job role.

Main functions:
- Improve resume wording
- Make resume more professional
- Align resume with job description
- Improve ATS keyword matching
- Avoid adding fake skills or experience

### 🎓 2. Course Recommendation Agent
Helps users identify learning topics and SkillsFuture search keywords.

Main functions:
- Analyze user career goal
- Identify learning areas
- Recommend skill areas
- Generate SkillsFuture search keywords
- Redirect users to MySkillsFuture search results

Important guardrail:

> The system avoids inventing fake course names.  
> It recommends learning topics and search keywords instead.

### 💼 3. Career / Job Advice Agent
Helps users explore suitable jobs and career pathways.

Main functions:
- Analyze resume or skill summary
- Suggest suitable job roles
- Identify skill gaps
- Suggest career transition pathways
- Provide practical job advice

### 🎤 4. Interview Preparation Agent
Helps users prepare for job interviews.

Main functions:
- Generate interview questions
- Provide suggested answer guidance
- Support technical and behavioural interview preparation
- Use job description and user background for better preparation

### 🛡️ 5. Policy & Privacy Agent
Provides privacy and safe usage guidance.

Main functions:
- Explain what users should not upload
- Remind users to remove sensitive information
- Encourage responsible AI usage

### 👤 6. Human Escalation Service
Allows users to submit a human support request.

Main functions:
- Collect user name and email
- Generate ticket number
- Send acknowledgement email
- Simulate a human escalation workflow

---

## 🏗️ System Architecture

```text
User
│
├── Streamlit Frontend
│
├── Flask Web Frontend
│
▼
Shared LangGraph Backend
│
├── Router Node
├── Resume Agent
├── Course Agent
├── Information Agent
├── Interview Agent
├── Policy Agent
└── Human Escalation Agent
│
▼
Groq LLM + RAG + FAISS + DuckDuckGo Search
```

---

## 🔄 LangGraph Workflow

The system uses **LangGraph** to manage multiple AI agents.

### Router Node

The router node reads the user query and decides which agent should answer.

Example routing:

| User Request | Routed To |
|---|---|
| “Rewrite my resume” | Resume Agent |
| “Recommend courses” | Course Agent |
| “What job suits me?” | Career / Job Advice Agent |
| “Prepare me for interview” | Interview Agent |
| “What data should I not upload?” | Policy Agent |
| “I need human help” | Human Escalation Agent |

---

## 🧩 Design Rationale

### Why LangGraph?
LangGraph was used because it supports:
- multi-agent workflows
- conditional routing
- modular agent design
- clearer system architecture

### Why Groq + Llama?
Groq was selected because:
- it is fast
- it supports Llama models
- it is beginner-friendly
- it works well for capstone prototypes

### Why FAISS?
FAISS was used because:
- it supports fast vector search
- it works locally
- it is suitable for RAG applications

### Why HuggingFace Embeddings?
The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This model was selected because:
- it is lightweight
- it is fast
- it works well for semantic search
- it is suitable for student projects and local development

### Why DuckDuckGo Search?
DuckDuckGo is used to support web-based discovery, especially for course-related search keywords and current information.

However, the system does not fully trust search results blindly.  
For course recommendations, the system avoids hallucinated course titles and provides SkillsFuture search keywords instead.

---

## 📁 Recommended Folder Structure

```text
CareerSkills-AI/
│
├── app.py
├── agents/
│   ├── resume_agent.py
│   ├── course_agent.py
│   ├── information_agent.py
│   ├── interview_agent.py
│   ├── policy_agent.py
│   └── human_escalation_agent.py
│
├── utils/
│   └── email_helper.py
│
├── db/
├── data/
├── data_raw/
│
├── streamlit_app/
│   ├── ui/
│   │   └── streamlit_app.py
│   └── static/
│
├── flask_web/
│   ├── web_app.py
│   ├── templates/
│   └── static/
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# ⚙️ Setup and Execution

## Step 1 — Open Project Folder

Open the project in VS Code.

```bash
cd CareerSkills-AI
```

## Step 2 — Create Virtual Environment

### macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Step 3 — Install Required Packages

```bash
pip install -r requirements.txt
```

## Step 4 — Create `.env` File

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_groq_api_key
EMAIL_USER=your_email@gmail.com
EMAIL_APP_PASSWORD=your_gmail_app_password
```

Important:
- Do not share your `.env` file
- Do not upload `.env` to GitHub
- Use Gmail App Password, not your normal Gmail password

## Step 5 — Run Streamlit Version

```bash
streamlit run streamlit_app/ui/streamlit_app.py
```

Expected result:
- Streamlit dashboard opens in browser
- User can select services from sidebar
- AI responses appear directly inside Streamlit

Common Streamlit URL:

```text
http://localhost:8501
```

## Step 6 — Run Flask Web Version

```bash
python flask_web/web_app.py
```

Expected result:

```text
Running on http://127.0.0.1:5000
```

Open in browser:

```text
http://127.0.0.1:5000
```

---

# 🧪 How To Test The System

## Test 1 — Resume Rewrite
1. Open Resume Rewrite page
2. Paste resume content or upload resume
3. Enter job title
4. Paste job description
5. Click Submit
6. Check rewritten resume response

Expected output:
- rewritten resume
- improved work experience
- clearer skills section
- final tailored resume draft

## Test 2 — Course Recommendation
1. Open Course Recommendation page
2. Enter resume or skill summary
3. Enter target role
4. Enter career goal
5. Click Submit

Expected output:
- learning topics
- skill areas
- SkillsFuture search keywords
- clickable MySkillsFuture search links

## Test 3 — Career / Job Advice
1. Open Career / Job Advice page
2. Paste resume or skill summary
3. Ask what jobs are suitable
4. Click Submit

Expected output:
- suitable job roles
- skill gaps
- career pathway suggestions

## Test 4 — Interview Preparation
1. Open Interview Preparation page
2. Enter target role
3. Paste job description
4. Ask for interview preparation
5. Click Submit

Expected output:
- technical questions
- behavioural questions
- suggested answer guidance

## Test 5 — Human Escalation
1. Open Human Escalation page
2. Fill in name, email, years of experience and request
3. Click Submit

Expected output:
- ticket number
- acknowledgement email sent to user

---

# 🔐 Privacy and Safety Notes

Users should not upload:
- NRIC / passport number
- bank details
- password
- home address
- date of birth
- phone number
- confidential company data

The system is for educational and career guidance purposes only.

---

# 🌈 Optional Enhancements Implemented

- Modern Flask UI
- Streamlit AI dashboard
- Clickable SkillsFuture search links
- Human escalation ticket workflow
- Email acknowledgement
- Resume upload support
- Markdown response formatting
- AI hallucination guardrails for course recommendation

---

# 📌 Colab Submission Note

For Colab submission, create Markdown cells at the top of the notebook with:

1. Project title
2. Author information
3. Problem statement
4. System architecture
5. Setup instructions
6. Agent workflow explanation
7. Design rationale
8. Usage instructions

This README content can be reused as the structured introduction in Colab.

---

# 🚀 Future Improvements

Possible future enhancements:
- real SkillsFuture API integration
- MyCareersFuture job search integration
- user login system
- database storage
- PDF export
- resume scoring
- chatbot memory
- admin dashboard
- deployment to Render or Hugging Face

---

# ✅ Conclusion

Career&Skills AI demonstrates how an AI support agent can be built using modern AI engineering concepts.

The project combines:
- agentic AI
- RAG
- LangGraph workflow
- LLM reasoning
- web frontend development
- email automation
- human escalation

This makes it suitable as a practical capstone project and a foundation for future AI career advisory platforms.


---

# 🏗️ Detailed System Architecture

## Overview

Career&Skills AI uses a **LangGraph multi-agent workflow architecture**.

Instead of using a single chatbot to answer every question, the system separates responsibilities into multiple specialized AI agents.

This architecture improves:
- modularity
- scalability
- maintainability
- routing clarity
- response specialization
- hallucination control

The system workflow is:

```text
User → Router Node → Specialized AI Agent → LLM + RAG → Final Response
```

---

# 🔄 LangGraph Workflow Architecture

## What is LangGraph?

LangGraph is a workflow orchestration framework designed for building AI systems with:
- multiple AI agents
- conditional routing
- state management
- sequential workflows
- branching logic

LangGraph works like a decision-making graph where:
- each node performs a task
- edges determine where the workflow moves next
- the state object carries information between nodes

In this project:
- every AI service is represented as a LangGraph node
- the Router Node decides which agent should answer the user

---

# 📌 Workflow Diagram

<img src="images/langgraph_workflow.png"
     width="100%">

This diagram visually shows:
- router logic
- conditional routing
- agent separation
- LLM integration
- RAG knowledge retrieval

---

# 🧠 Router Node

## Purpose

The Router Node acts as the central controller of the system.

It:
- reads the user query
- detects user intent
- decides which agent should handle the request

---

## Why Use A Router?

Without a router:
- every AI agent would receive every request
- responses become inconsistent
- higher hallucination risk
- slower processing

Using a router improves:
- specialization
- performance
- explainability
- workflow transparency

---

## Example Router Logic

Example query:

```text
"Please rewrite my resume for a Data Analyst role."
```

Router detects keywords:
- rewrite
- resume

Workflow routing:

```text
User → Router Node → Resume Agent
```

---

# 📄 Resume Agent Node

## Purpose

The Resume Agent specializes in:
- resume rewriting
- ATS optimization
- keyword enhancement
- job description alignment

---

## Inputs

The Resume Agent receives:
- user resume
- target job title
- job description
- rewrite instruction

---

## Outputs

Example outputs:
- rewritten professional summary
- optimized work experience
- ATS keywords
- tailored resume draft

---

## Example Workflow

```text
User Upload Resume
        ↓
Resume Agent
        ↓
Groq LLM
        ↓
Optimized Resume Response
```

---

# 🎓 Course Recommendation Agent Node

## Purpose

This agent specializes in:
- upskilling guidance
- learning pathways
- skill gap analysis
- SkillsFuture recommendations

---

## Important Hallucination Guardrail

A key design decision was implemented:

❌ The system avoids generating fake course names.

Instead, the system recommends:
- learning topics
- skill areas
- certification areas
- SkillsFuture search keywords

This reduces hallucination risks.

---

## Example Workflow

```text
User Career Goal
        ↓
Course Agent
        ↓
DuckDuckGo Search + RAG
        ↓
SkillsFuture Search Keywords
```

---

# 💼 Career / Job Advice Agent Node

## Purpose

This agent specializes in:
- career recommendations
- suitable job roles
- career transitions
- industry matching

---

## Inputs

The agent receives:
- user resume
- user skill summary
- user career question

---

## Example

User question:

```text
"What jobs are suitable for someone with Python and SQL?"
```

Possible response:
- Data Analyst
- Business Intelligence Analyst
- Junior AI Engineer

---

# 🎤 Interview Preparation Agent Node

## Purpose

This agent helps users prepare for interviews.

Functions include:
- technical interview preparation
- behavioural interview preparation
- role-specific guidance
- answer structuring

---

## Inputs

The Interview Agent receives:
- target role
- job description
- user background
- interview question

---

## Example

```text
Target Role:
AI Engineer

Job Description:
Machine learning, Python, SQL
```

Generated output:
- interview questions
- answer suggestions
- important technical topics

---

# 🛡️ Policy Agent Node

## Purpose

This node provides:
- AI safety guidance
- privacy education
- responsible upload reminders

---

## Example Guidance

The Policy Agent reminds users not to upload:
- NRIC
- bank information
- passwords
- confidential company data

---

# 👤 Human Escalation Agent Node

## Purpose

This node handles:
- support ticket generation
- human escalation workflows
- acknowledgement emails

---

## Workflow

```text
User submits request
        ↓
Ticket Number Generated
        ↓
Acknowledgement Email Sent
```

---

# 🔀 Conditional Edges

## What Are Conditional Edges?

Conditional edges determine:
> where the workflow should go next.

The Router Node checks:
- keywords
- user intent

Then routes to the appropriate node.

---

## Example Conditional Routing

| User Query | Selected Node |
|---|---|
| "Rewrite my CV" | Resume Agent |
| "Recommend courses" | Course Agent |
| "Prepare me for interview" | Interview Agent |
| "I need human support" | Human Escalation Agent |

---

# 📦 Shared State Object

LangGraph uses a shared state object.

The state carries:
- user query
- resume text
- job description
- target role
- career goal
- generated response

between nodes.

---

# 🎯 Why This Architecture Was Chosen

This architecture was selected because it is:
- modular
- scalable
- easy to debug
- beginner-friendly
- enterprise-inspired

Advantages:
- each agent has a specialized responsibility
- easier future expansion
- easier maintenance
- reduced hallucination
- cleaner code organization

---

# 🚀 Future Architectural Improvements

Potential future improvements include:
- semantic intent classification
- confidence-based routing
- memory-enabled conversation flow
- multi-step reasoning chains
- database persistence
- API integrations
- recruiter matching engine

---

# ✅ Architecture Summary

The LangGraph architecture enables Career&Skills AI to behave like a coordinated AI ecosystem instead of a single chatbot.

The workflow:
- improves specialization
- improves maintainability
- improves response quality
- reduces hallucination risks
- provides enterprise-style AI orchestration


---

# 🧩 Design Rationale

## Overall Design Philosophy

<img src="images/Architecture_Design_Summary.png"
     width="100%">

Career&Skills AI was designed using a modular multi-agent architecture instead of a single chatbot architecture.

The objective was to simulate a realistic enterprise AI support system where:
- different AI agents specialize in different tasks
- routing logic determines the most suitable expert agent
- RAG retrieval improves contextual responses
- the frontend behaves like a real online support platform

The system was intentionally designed to balance:
- AI capability
- educational simplicity
- scalability
- modularity
- user experience
- hallucination mitigation

---

# 🎯 Why Two Different Versions Were Developed

Two separate frontend versions were intentionally created for learning and comparison purposes.

## 1. Streamlit Version

The Streamlit version was designed primarily for:
- rapid prototyping
- fast AI testing
- easier debugging
- beginner-friendly experimentation

### Why Streamlit Was Chosen

Advantages:
- very fast development
- minimal frontend coding required
- ideal for AI experimentation
- easy integration with Python AI libraries
- suitable for proof-of-concept demonstrations

The Streamlit version allowed the project to:
- quickly validate the LangGraph workflow
- test prompts and agent logic
- experiment AI functionality rapidly

---

## 2. Flask Web Version

The Flask version was designed to simulate a more realistic production-style web application.

### Why Flask Was Chosen

Flask was selected because it provides:
- flexible backend routing
- HTML/CSS/JavaScript integration
- real web development experience
- customizable UI structure
- separation between frontend and backend logic

This version better simulates:
- enterprise web applications
- customer support portals
- online AI service platforms

---

# 🔄 Shared Backend Architecture

Although two frontend versions were created, both versions share the same backend architecture.

Shared components include:
- LangGraph workflow
- AI agents
- RAG vector database
- embedding model
- LLM integration
- utility functions
- prompt engineering logic

This demonstrates:
- backend reusability
- separation of concerns
- scalable architecture design

---

# 🧠 Why LangGraph Was Selected

LangGraph was selected because the project required:
- multiple AI agents
- workflow orchestration
- conditional routing
- state management
- modular execution flow

Instead of building one large chatbot, the system was designed as multiple specialized AI agents.

This improves:
- maintainability
- modularity
- debugging
- scalability
- response specialization

---

# 🔀 Why Keyword-Based Routing Was Used

The Router Node currently uses keyword-based intent routing.

Example:
- "resume" → Resume Agent
- "course" → Course Agent
- "interview" → Interview Agent

Advantages:
- simple implementation
- easy debugging
- beginner-friendly
- transparent routing logic
- lightweight execution

---

# 🤖 Why Groq + Llama 3.1 Was Selected

Groq was selected because:
- very fast inference speed
- free developer access
- easy API integration

Llama 3.1 was selected because:
- good reasoning capability
- strong instruction following
- high-quality text generation

---

# 📚 Why RAG Was Implemented

RAG (Retrieval-Augmented Generation) was implemented to:
- improve response relevance
- reduce hallucination
- provide contextual grounding

---

# 🧠 Why FAISS Was Selected

FAISS was chosen because:
- fast vector similarity search
- lightweight local deployment
- suitable for educational projects

---

# 🔍 Why all-MiniLM-L6-v2 Embedding Model Was Selected

The project uses:
sentence-transformers/all-MiniLM-L6-v2

Reasons:
- lightweight
- fast
- efficient
- low memory usage
- good semantic similarity performance

---

# 🌐 Why DuckDuckGo Search Was Used

DuckDuckGo Search was integrated to:
- provide lightweight web search capability
- support SkillsFuture keyword discovery
- improve recommendation freshness

---

# 🛡️ Hallucination Mitigation Design

To reduce hallucination risk:
- the Course Agent avoids inventing fake course names
- recommends learning topics instead
- generates SkillsFuture search keywords
- redirects users to official MySkillsFuture search

---

# 🎨 Frontend Design Choices

The frontend was designed to:
- feel modern and approachable
- resemble professional AI platforms
- improve readability
- simplify user interaction

Features include:
- sidebar navigation
- service-based pages
- hero banners
- markdown AI formatting
- clickable SkillsFuture links

---

# 📧 Human Escalation Workflow Design

The Human Escalation workflow simulates:
- enterprise support escalation
- ticket management systems
- customer service workflows

Features:
- ticket generation
- acknowledgement email
- request tracking simulation

---

# 🚀 Scalability Considerations

Possible future upgrades:
- API-based architecture
- cloud deployment
- database persistence
- chatbot memory
- recruiter integration
- authentication system

---

# ✅ Design Summary

Career&Skills AI demonstrates:
- LangGraph orchestration
- multi-agent AI architecture
- RAG integration
- Flask web engineering
- Streamlit prototyping
- hallucination mitigation
- enterprise-inspired AI workflow

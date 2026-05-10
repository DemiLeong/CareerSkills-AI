# Career&Skills AI — Implementation Guidelines

## Purpose of This Document

This document provides step-by-step implementation guidance for setting up, configuring, running, testing, and demonstrating the Career&Skills AI system.

The system is designed as an AI-powered online support agent for career services, resume support, course recommendation, interview preparation, policy guidance, and human escalation support.

---

# Important Security Note

Before uploading the project to GitHub:

## Do NOT upload your real `.env` file

Your `.env` file may contain:
- Groq API key
- Gmail address
- Gmail App Password
- other private credentials

These should never be uploaded to GitHub.

---

## Recommended GitHub Setup

Add this into `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
.DS_Store
```

Create a safe example file:

```text
.env.example
```

Example content:

```env
GROQ_API_KEY=your_groq_api_key_here
EMAIL_USER=your_email_here
EMAIL_APP_PASSWORD=your_gmail_app_password_here
```

Users can copy it:

```bash
cp .env.example .env
```

Then replace the placeholder values with their own credentials.

---

# Step 1: Environment and Knowledge Base Setup

## 1.1 Create Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 1.2 Install All Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

Important packages include:

```text
flask
streamlit
langgraph
langchain
langchain-community
langchain-huggingface
faiss-cpu
sentence-transformers
groq
duckduckgo-search
python-dotenv
python-docx
pypdf
markdown
```

---

## 1.3 Configure Chosen LLM

This project uses:

```text
Groq API + Llama 3.1
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
EMAIL_USER=your_email_here
EMAIL_APP_PASSWORD=your_gmail_app_password_here
```

The Groq API key is used by AI agents to call the LLM.

The email details are used by the Human Escalation service to send acknowledgement emails.

---

# Step 2: Knowledge Base Construction

The project uses a Retrieval-Augmented Generation approach.

The knowledge base is built from files stored in the `/data/` directory.

---

## 2.1 Read Data Files

The ingestion script reads text documents from the `/data/` directory.

Example folders may include:

```text
data/
├── jobs/
├── courses/
└── policy/
```

Each category can be converted into a separate vector database collection.

---

## 2.2 Split Text Into Chunks

Large text files are split into smaller chunks before embedding generation.

Recommended chunking approach:

```text
chunk_size = 800 to 1000 characters
chunk_overlap = 100 to 200 characters
```

Why chunking is needed:
- improves retrieval accuracy
- avoids exceeding model context limits
- allows more focused search results

---

## 2.3 Generate Embeddings

This project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Reasons for selection:
- lightweight
- fast
- suitable for local development
- good semantic similarity performance
- works well with FAISS

---

## 2.4 Store Embeddings In Vector Database

The project uses:

```text
FAISS
```

The embeddings are stored inside the `/db/` directory.

Recommended structure:

```text
db/
├── jobs/
├── courses/
└── policy/
```

Separate collections are useful because:
- faster targeted retrieval
- easier maintenance
- clearer separation of knowledge domains

---

## 2.5 Expected Output

After running the ingestion process, the expected output is:

```text
db/
├── jobs/
│   ├── index.faiss
│   └── index.pkl
│
├── courses/
│   ├── index.faiss
│   └── index.pkl
│
└── policy/
    ├── index.faiss
    └── index.pkl
```

This means the vector database is ready for retrieval.

---

# Step 3: LangGraph Workflow Development

The project uses LangGraph to coordinate multiple specialized AI agents.

---

## 3.1 Define the State

A `TypedDict` is used to define the graph state.

Example:

```python
class CareerSkillsState(TypedDict):
    query: str
    resume_text: str
    job_description: str
    job_title: str
    target_role: str
    career_goal: str
    next_node: str
    response: str
    resume_mode: str
```

The state stores:
- user query
- resume text
- job description
- target role
- career goal
- router decision
- final AI response

---

## 3.2 Create Agent Nodes

Each AI service is implemented as a separate node.

Main nodes:

| Node | Purpose |
|---|---|
| Resume Node | Rewrite and optimize resumes |
| Course Node | Recommend learning topics and SkillsFuture keywords |
| Information Node | Provide career and job advice |
| Interview Node | Generate interview preparation guidance |
| Policy Node | Provide privacy and safe usage guidance |
| Human Escalation Node | Handle requests that need human support |

Each node calls its respective agent function.

Example:

```python
def resume_node(state):
    response = resume_agent(
        state["resume_text"],
        state["job_title"],
        state["job_description"]
    )

    return {
        **state,
        "response": response
    }
```

---

## 3.3 Implement the Router Node

The router node decides which agent should respond.

In this project, a keyword-based routing strategy was used for simplicity and transparency.

Example logic:

```text
resume / cv         → Resume Agent
course / upskill    → Course Agent
career / job        → Career Agent
interview           → Interview Agent
privacy / policy    → Policy Agent
human / advisor     → Human Escalation Agent
```

Although the assignment mentions LLM-based semantic classification, this project currently uses keyword-based routing because:
- easier to explain
- easier to debug
- reliable for defined service categories
- suitable for educational capstone scope

Future enhancement:
- replace keyword routing with LLM semantic routing
- add confidence scores
- route low-confidence cases to Human Escalation

---

## 3.4 Human Escalation Node

The Human Escalation Node acts as the system fail-safe.

It is triggered when:
- user explicitly asks for human help
- user asks for advisor support
- user asks for escalation
- query is too complex or sensitive

In the Flask version, Human Escalation collects:
- title
- first name
- last name
- email
- years of experience
- request description

Then the system:
- generates a ticket number
- sends an acknowledgement email
- displays confirmation to the user

---

# Step 4: Graph Construction and Compilation

## 4.1 Instantiate StateGraph

```python
workflow = StateGraph(CareerSkillsState)
```

---

## 4.2 Add Nodes

```python
workflow.add_node("router", router_node)
workflow.add_node("resume", resume_node)
workflow.add_node("course", course_node)
workflow.add_node("information", information_node)
workflow.add_node("interview", interview_node)
workflow.add_node("policy", policy_node)
workflow.add_node("human", human_node)
```

---

## 4.3 Set Entry Point

```python
workflow.set_entry_point("router")
```

The router node is always the first node.

---

## 4.4 Add Conditional Edges

Conditional edges route the graph based on `next_node`.

```python
workflow.add_conditional_edges(
    "router",
    lambda state: state["next_node"],
    {
        "resume": "resume",
        "course": "course",
        "information": "information",
        "interview": "interview",
        "policy": "policy",
        "human": "human",
    }
)
```

---

## 4.5 Add End Edges

Each agent node ends the workflow after generating a response.

```python
workflow.add_edge("resume", END)
workflow.add_edge("course", END)
workflow.add_edge("information", END)
workflow.add_edge("interview", END)
workflow.add_edge("policy", END)
workflow.add_edge("human", END)
```

---

## 4.6 Compile Workflow

```python
careerskills_app = workflow.compile()
```

The compiled app is then used by Flask and Streamlit.

---

# Step 5: Testing and Demonstration

The final system should be tested with multiple types of user requests.

---

## 5.1 Resume Rewrite Test

Example:

```text
Please rewrite my resume for a Data Analyst role.
```

Expected:
- Resume Agent selected
- rewritten professional resume generated
- no fake skills added

---

## 5.2 Course Recommendation Test

Example:

```text
I want to become a WSQ Trainer. What should I learn?
```

Expected:
- Course Agent selected
- learning topics generated
- SkillsFuture search keywords generated
- clickable MySkillsFuture links provided

---

## 5.3 Career Advice Test

Example:

```text
What jobs are suitable for someone with Python, SQL and Excel?
```

Expected:
- Information Agent selected
- suitable roles suggested
- skill gaps identified

---

## 5.4 Interview Preparation Test

Example:

```text
Prepare me for a Data Analyst interview.
```

Expected:
- Interview Agent selected
- technical and behavioural questions generated

---

## 5.5 Policy Question Test

Example:

```text
What personal information should I not upload?
```

Expected:
- Policy Agent selected
- safe usage guidance displayed

---

## 5.6 Human Escalation Test

Example:

```text
I need a human advisor to review my resume.
```

Expected:
- Human Escalation page used
- ticket generated
- acknowledgement email sent

---

# Running the Applications

## Main Flask Version

Run:

```bash
python flask_web/web_app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Streamlit Prototype Version

Run:

```bash
streamlit run streamlit_app/ui/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

# Can `python app.py` Run Both Versions?

No.

`app.py` is used as the shared LangGraph backend logic.

The two frontend versions must be launched separately:

| Version | Command |
|---|---|
| Flask Web Version | `python flask_web/web_app.py` |
| Streamlit Version | `streamlit run streamlit_app/ui/streamlit_app.py` |

They can run at the same time in two terminals because they use different ports.

---

# Final Expected Deliverables

Recommended submission package:

```text
CareerSkills-AI/
├── README.md
├── IMPLEMENTATION_GUIDELINES.md
├── requirements.txt
├── .env.example
├── agents/
├── flask_web/
├── streamlit_app/
├── utils/
├── data/
├── db/
└── images/
```

---

# Summary

This implementation guide explains how to:
- install dependencies
- configure the LLM
- build the RAG knowledge base
- generate embeddings
- store vectors in FAISS
- define LangGraph state
- create agent nodes
- implement routing
- compile the workflow
- run and test both Flask and Streamlit versions

The project demonstrates a full AI agentic workflow suitable for an online support agent capstone project.

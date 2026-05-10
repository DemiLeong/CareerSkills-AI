from typing import TypedDict, cast

from langgraph.graph import StateGraph, END

from agents.resume_agent import resume_agent
from agents.course_agent import course_agent
from agents.information_agent import information_agent
from agents.policy_agent import policy_agent
from agents.human_escalation_agent import human_escalation_agent
from agents.interview_agent import interview_agent


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


def router_node(state: CareerSkillsState):
    query = state["query"].lower()

    # Human Escalation first
    if "human" in query or "advisor" in query or "escalate" in query:
        next_node = "human"

    # Career / Job Advice before Resume
    elif (
        "career" in query
        or "job advice" in query
        or "job matching" in query
        or "job recommendation" in query
        or "suitable job" in query
        or "suitable role" in query
        or "what job" in query
        or "what jobs" in query
        or "career transition" in query
    ):
        next_node = "information"

    # Resume only when user explicitly asks to rewrite/improve resume
    elif (
        "rewrite resume" in query
        or "resume rewrite" in query
        or "improve resume" in query
        or "tailor resume" in query
        or "rewrite cv" in query
        or "improve cv" in query
    ):
        next_node = "resume"

    elif "course" in query or "upskill" in query or "learn" in query:
        next_node = "course"

    elif "interview" in query:
        next_node = "interview"

    elif "privacy" in query or "policy" in query or "upload" in query:
        next_node = "policy"

    else:
        next_node = "information"

    print("ROUTER QUERY:", query)
    print("ROUTED TO:", next_node)

    return {
        **state,
        "next_node": next_node
    }


def resume_node(state: CareerSkillsState):
    response = resume_agent(
        state["resume_text"],
        state["job_title"],
        state["job_description"]
    )
    return {**state, "response": response}


def course_node(state: CareerSkillsState):
    response = course_agent(
        state["resume_text"],
        state["target_role"],
        state["career_goal"]
    )
    return {**state, "response": response}


def information_node(state: CareerSkillsState):
    response = information_agent(
        state["query"],
        state["resume_text"]
    )
    return {**state, "response": response}


def policy_node(state: CareerSkillsState):
    response = policy_agent(state["query"])
    return {**state, "response": response}


def human_node(state: CareerSkillsState):
    response = human_escalation_agent(
        state["query"],
        reason="Router detected that this request may require human support."
    )
    return {**state, "response": response}


def interview_node(state: CareerSkillsState):
    response = interview_agent(
        target_role=state["target_role"],
        user_background=state["resume_text"],
        interview_type=state["query"],
        job_description=state["job_description"]
    )
    return {**state, "response": response}


def build_graph():
    workflow = StateGraph(CareerSkillsState)

    workflow.add_node("router", router_node)
    workflow.add_node("resume", resume_node)
    workflow.add_node("course", course_node)
    workflow.add_node("information", information_node)
    workflow.add_node("policy", policy_node)
    workflow.add_node("human", human_node)
    workflow.add_node("interview", interview_node)

    workflow.set_entry_point("router")

    workflow.add_conditional_edges(
        "router",
        lambda state: state["next_node"],
        {
            "resume": "resume",
            "course": "course",
            "information": "information",
            "policy": "policy",
            "human": "human",
            "interview": "interview",
        }
    )

    workflow.add_edge("resume", END)
    workflow.add_edge("course", END)
    workflow.add_edge("information", END)
    workflow.add_edge("policy", END)
    workflow.add_edge("human", END)
    workflow.add_edge("interview", END)

    return workflow.compile()


careerskills_app = build_graph()


if __name__ == "__main__":

    test_state = {
        "query": "Recommend courses for AI Engineer",
        "resume_text": """
Skills: Python, SQL, Excel
Experience: Junior analyst building dashboards.
""",
        "job_description": """
AI Engineer role requiring Python and machine learning.
""",
        "job_title": "AI Engineer",
        "target_role": "AI Engineer",
        "career_goal": "Transition into AI Engineer",
        "resume_mode": "advice",
        "next_node": "",
        "response": ""
    }

    result = careerskills_app.invoke(
        cast(CareerSkillsState, test_state)
    )

    print("\nCareerSkills AI - LangGraph Test")
    print("-" * 60)
    print("Selected Agent:", result["next_node"])
    print("-" * 60)
    print(result["response"])
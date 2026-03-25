"""LangGraph research agent with reflection loops."""
from __future__ import annotations
import operator
from typing import Annotated, List, TypedDict, Optional
from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver


class ResearchState(TypedDict):
    query: str
    findings: Annotated[List[str], operator.add]
    sources: Annotated[List[str], operator.add]
    gaps: List[str]
    iteration: int
    max_iterations: int
    report: str
    approved: bool


def should_continue_research(state: ResearchState) -> str:
    if state.get("approved") or state["iteration"] >= state["max_iterations"]:
        return "write"
    return "research"


def build_research_graph(researcher=None, critic=None, writer=None):
    from src.agents import ResearchAgent, CriticAgent, WriterAgent
    researcher = researcher or ResearchAgent()
    critic = critic or CriticAgent()
    writer = writer or WriterAgent()

    workflow = StateGraph(ResearchState)
    workflow.add_node("researcher", researcher.run)
    workflow.add_node("critic", critic.run)
    workflow.add_node("writer", writer.run)

    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "critic")
    workflow.add_conditional_edges("critic", should_continue_research, {"research": "researcher", "write": "writer"})
    workflow.add_edge("writer", END)

    return workflow.compile(checkpointer=MemorySaver())

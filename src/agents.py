"""Research, critic, and writer agents."""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults

RESEARCH_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a thorough research assistant. Search for information on the topic and gaps provided. Return key findings with source URLs."),
    ("human", "Topic: {query}\nGaps to address: {gaps}\n\nResearch these areas and return bullet-point findings with sources:")
])
CRITIC_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a critical research reviewer. Identify gaps, weaknesses, and missing angles in the research."),
    ("human", "Query: {query}\nFindings so far:\n{findings}\n\nIdentify gaps. If research is comprehensive, say APPROVED. Otherwise list specific gaps:")
])
WRITER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Synthesize findings into a professional report with executive summary, key findings, and citations."),
    ("human", "Query: {query}\nFindings:\n{findings}\nSources:\n{sources}\n\nWrite a comprehensive research report:")
])


class ResearchAgent:
    def __init__(self, model="gpt-4o"):
        self.llm = ChatOpenAI(model=model, temperature=0.1)
        self.chain = RESEARCH_PROMPT | self.llm
        try:
            self.search = TavilySearchResults(max_results=5)
        except Exception:
            self.search = None

    def run(self, state):
        gaps = state.get("gaps", [])
        result = self.chain.invoke({"query": state["query"], "gaps": gaps or "Initial research"})
        new_findings = [result.content]
        new_sources = []
        if self.search:
            try:
                search_results = self.search.invoke(state["query"])
                new_sources = [r.get("url","") for r in search_results if isinstance(r, dict)]
            except Exception:
                pass
        return {"findings": new_findings, "sources": new_sources, "iteration": state.get("iteration",0) + 1}


class CriticAgent:
    def __init__(self, model="gpt-4o"):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.chain = CRITIC_PROMPT | self.llm

    def run(self, state):
        result = self.chain.invoke({"query": state["query"], "findings": "\n".join(state.get("findings",[]))})
        approved = "APPROVED" in result.content.upper()
        gaps = [] if approved else [result.content]
        return {"gaps": gaps, "approved": approved}


class WriterAgent:
    def __init__(self, model="gpt-4o"):
        self.llm = ChatOpenAI(model=model, temperature=0.2)
        self.chain = WRITER_PROMPT | self.llm

    def run(self, state):
        result = self.chain.invoke({"query": state["query"], "findings": "\n".join(state.get("findings",[])), "sources": "\n".join(state.get("sources",[]))})
        return {"report": result.content}

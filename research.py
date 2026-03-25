"""Research agent CLI entry point."""
import sys, asyncio
from src.graph import build_research_graph

async def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is LangGraph and how does it work?"
    print(f"Researching: {query}\n{'='*60}")
    graph = build_research_graph()
    result = await asyncio.to_thread(graph.invoke, {
        "query": query, "findings": [], "sources": [], "gaps": [], "iteration": 0, "max_iterations": 3, "report": ""
    })
    print(result.get("report", "No report generated"))

if __name__ == "__main__":
    asyncio.run(main())

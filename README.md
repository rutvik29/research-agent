# 🔬 Research Agent

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2-FF6B35?style=flat)](https://langchain-ai.github.io/langgraph/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Deep research agent** with LangGraph reflection loops — searches the web, reads papers, identifies gaps, synthesizes findings, and delivers cited reports with confidence scores.

## ✨ Highlights

- 🔍 **Multi-source search** — Tavily, Arxiv, Wikipedia, and web scraping
- 🔄 **Reflection loops** — critiques its own research, identifies gaps, re-searches
- 📝 **Structured reports** — executive summary, findings, methodology, citations
- 📊 **Confidence scoring** — rates each claim with source quality assessment
- 🧵 **Parallel research** — searches multiple angles simultaneously
- 📚 **Arxiv integration** — reads and summarizes academic papers

## Architecture

```
Research Query
      │
      ▼
┌───────────────┐    ┌──────────────┐    ┌──────────────┐
│  Planner      │───▶│  Researcher  │───▶│  Critic      │
│ (decompose)   │    │ (search+read)│    │ (gap-finder) │
└───────────────┘    └──────────────┘    └──────┬───────┘
                           ▲                    │
                           └────────────────────┘
                              (reflection loop)
                                    │ (approved)
                             ┌──────▼───────┐
                             │  Writer      │
                             │ (final report)│
                             └──────────────┘
```

## Quick Start

```bash
git clone https://github.com/rutvik29/research-agent
cd research-agent
pip install -r requirements.txt
cp .env.example .env

python research.py "What are the latest breakthroughs in protein folding AI?"
```

## Example Output

```markdown
# Research Report: Protein Folding AI Breakthroughs

## Executive Summary
AlphaFold 3 (May 2024) extends structure prediction to all biomolecules...

## Key Findings
1. **AlphaFold 3** — 50% improvement on protein-ligand interactions [Confidence: 0.96]
2. **ESM3** — Multimodal protein language model generating novel proteins [Confidence: 0.91]

## Sources
- [Abramson et al. 2024] AlphaFold 3... (Nature, May 2024)
```

## License
MIT © Rutvik Trivedi

# System Architecture & Core Pipelines

This document outlines the end-to-end data processing pipeline for generating deep contributor metrics.

## 1. Data Ingestion & Rate-Limit Resiliency
The system interfaces directly with GitHub's GraphQL API. To combat strict GitHub rate limiting, we implement a **Leaky Bucket token bucket algorithm** using Redis.
- Long-running repository analysis tasks are chunked into micro-batches.
- Commits are queried chronologically backwards, parsing only structural metadata before fetching full diffs.

[GitHub API] ──> [Redis Queue] ──> [Worker Pool] ──> [Database]

## 2. Dynamic Metric Calculation Formula (The Core Algorithm)

An engineering contribution score ($CS$) is computed mathematically to eliminate padding commits (e.g., typos, formatting adjustments):

$$CS = \sum_{c \in Commits} \left( \alpha \cdot \Delta AST_c + \beta \cdot C_{complexity} + \gamma \cdot S_{weight} \right)$$

Where:
- $\Delta AST_c$: Structural changes in the code tree (ignores whitespace, variable renames).
- $C_{complexity}$: Cyclomatic complexity reduction value parsed by Tree-sitter.
- $S_{weight}$: Security modifier multiplier (triggered if the commit resolves an issue tagged with CVE/Security keywords).

## 3. The AI Verification Pipeline
Raw git diffs are often noisy. Our AI Agent processing chain follows these isolated steps:
1. **Filtering:** Diffs over 200 lines are pre-filtered to remove boilerplate or lockfile updates.
2. **Context Enrichment:** The agent receives the target function's parent structure, the commit message, and closed issue descriptions.
3. **Inference:** The LLM categorizes the impact into one of 5 vectors: *Optimiza

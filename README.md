<img width="2760" height="368" alt="image" src="https://github.com/user-attachments/assets/c869e67b-77ec-4004-b78e-af2bde6f696a" />

  ## 🚀 GitImpact
  ### *Beyond the Green Squares: AI-Powered Semantic Portfolios for Open-Source Contributors*

  [![License: MIT](https://shields.io)](https://opensource.org)
  [![CI Pipeline](https://github.com)](https://github.com)
  [![PRs Welcome](https://shields.io)](http://makeapullrequest.com)
  [![Built with Python](https://shields.io)](https://github.com)

  **GitImpact** is a next-generation developer analytics engine that scans public GitHub repositories to calculate the **true quantitative and qualitative value** of an engineer's lifetime work. 
  
  *Stop counting trivial commits. Start measuring actual engineering impact.*

  [Explore Architecture](#-architecture--deep-dive) •
  [Key Features](#-key-features) •
  [Getting Started](#-quick-start) •
  [Contribute](#-contributing)
</div>

---

## 💡 Why GitImpact?

The current GitHub profile fallback mechanism (the famous contribution green wall) treats a **one-character typo fix** exactly the same as a **complex architectural multi-threading memory leak patch**. This creates a massive misalignment for technical recruiters and engineering managers looking for real talent.

GitImpact solves this by dissecting git history, extracting modified code blocks, parsing syntax states, and leveraging advanced Large Language Models to generate an interactive, semantic, and highly analytical professional engineering resume.

---

## ✨ Key Features

### 🌲 AST-Based Code Profiling (No Noise)
Leverages a customized `tree-sitter` compilation parser to calculate the **Cyclomatic Complexity Delta** of every code modification. If a contributor optimizes code, the system mathematically detects structural reductions, ignoring whitespace, formatting shifts, or variable renames.

### 🤖 OpenAI-Structured Semantic Inference
Utilizes OpenAI’s **Structured Outputs API** to process complex code diffs into human-readable engineering achievements. Diffs are classified into 5 major categories: *Optimization, Security, Architecture, Maintainability, and Bugfixes*.

### 🔍 Natural Language Recruitment Discovery
Powered by a fully decentralized vector storage engine (`pgvector`), allowing engineering managers to query portfolios using raw intent:
> *"Find me candidates from this organization who have written low-latency caching structures or fixed critical security vulnerabilities."*

### 🛡️ Built-In Resilience Rate Limiter
Features a high-throughput **Leaky Bucket algorithm** executed through asynchronous Redis memory states. It guarantees absolute node protection against intense GitHub GraphQL API rate blocks.

---

## 🗺️ Architecture & Data Pipelines

The system is engineered as a decoupled, high-performance monorepo utilizing background worker orchestration queues to stay cost-effective and ultra-fast.

```
                  ┌───────────────────────┐
                  │   GitHub GraphQL API  │
                  └───────────┬───────────┘
                              │ 
                [Token Leaky Bucket / Redis]
                              ▼
                  ┌───────────────────────┐
                  │    Ingestion Engine   │
                  └───────────┬───────────┘
                              ▼
                [AST Structural Pre-Filter]
                              ▼
                  ┌───────────────────────┐
                  │   LLM Inference Layer │
                  └───────────┬───────────┘
                              ▼
         ┌────────────────────┴────────────────────┐
         ▼                                         ▼
┌──────────────────┐                      ┌──────────────────┐
│ PostgreSQL Relational                     │ pgvector Cluster │
└──────────────────┘                      └──────────────────┘
```

---

## 📂 Repository Structure

```text
├── .github/
│   └── workflows/          # Automated GitHub CI/CD build actions
├── apps/
│   ├── api/                # High-performance FastAPI (Python 3.11) backend
│   │   ├── engine/         # core ingestion, rate-limiting & embedding engines
│   │   ├── workers/        # background async execution tasks
│   │   └── tests/          # isolated integration testing suite
│   └── web/                # Next.js 14 Web UI Dashboard Interface
├── packages/
│   └── ast-analyzer/       # Node.js TypeScript Abstract Syntax Tree parser
├── docker-compose.yml      # Universal zero-config multi-service infrastructure
├── .env.example            # Environment variables credential blueprints
└── README.md               # Repository documentation storefront
```

---

## 🚀 Quick Start

### Prerequisites
Ensure you have the following software foundations initialized locally:
* **Docker & Docker Compose**
* **Node.js** >= 18.x
* **Python** >= 3.11
* An **OpenAI API Key** and a **GitHub Personal Access Token (PAT)**

### Installation & Initialization

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd gitimpact
   ```

2. **Configure environmental secrets:**
   ```bash
   cp .env.example .env
   # Open .env and populate your OPENAI_API_KEY and GITHUB_ACCESS_TOKEN
   ```

3. **Spin up the complete decoupled infrastructure via Docker:**
   ```bash
   docker-compose up --build -d
   ```
   *This single command automatically activates the pgvector instance, setups Redis, builds the Node-Python hybrid microservices, and boots the backend pipeline.*

4. **Verify running containers status:**
   ```bash
   docker ps
   ```

---

## 🧪 Running The Testing Suites

To ensure architectural integrity, tests are decoupled across runtimes. The backend suite checks core mock ingestion flows and embedding alignment vector rules.

```bash
# Executing Python Core Engine tests
pytest apps/api/tests/

# Executing TypeScript AST Parser tests
npm run test --workspace=packages/ast-analyzer
```

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

  *Crafted with 🧠 and engineered for the global open-source community.*
</div>

# Local AI Agent System

A fully local, modular AI agent system built on LangChain and Ollama-compatible models. It acts as a personal AI assistant capable of conversation, reasoning, coding, image analysis, image generation, and tool use, while building a long-term memory of the user over time.

The objective is not to build another chatbot, but a continuously learning local AI system that develops memory, skills, preferences, and domain knowledge over time while remaining modular and controllable.

## Project Structure

```
local-agent/
├── agents/
│   ├── ChatAgent.py          # General conversation
│   ├── ClassifierAgent.py    # Routes incoming requests
│   ├── CodingAgent.py        # Software engineering tasks
│   ├── ImageAgent.py         # Image generation
│   ├── LogicalAgent.py       # Reasoning-heavy tasks
│   ├── MemoryAgent.py        # Updates memory after each interaction
│   ├── PlannerAgent.py       # Step-by-step plans for complex tasks
│   ├── VerifierAgent.py      # Reviews output before it reaches the user
│   └── VisionAgent.py        # Image analysis (OCR, screenshots, UI)
├── config/
│   └── model_config.py       # Model and provider configuration
├── memory/
│   ├── chat/
│   │   └── chat.md           # Saved conversation summaries
│   ├── facts/
│   │   └── facts.md          # Objective facts about the user
│   ├── interest/
│   │   └── interest.md       # Long-term interests
│   ├── profile/
│   │   └── profile.md        # Identity and preferences
│   └── skills/
│       └── skills.md         # Learned workflows and preferences
├── tools/
│   ├── Browsing.py           # Web search and page reading
│   ├── FileSystem.py         # Local file read/write
│   ├── Memory.py             # Search/retrieve from the LLM Wiki
│   └── Terminal.py           # Shell command execution
└── README.md
```

## Architecture

```
User Query
   │
   ▼
ClassifierAgent
   │  decides: which agent, whether planning is required, whether tools are required
   ▼
PlannerAgent (optional)
   │  creates an execution plan for complex tasks
   ▼
Selected Agent
   (Chat / Coding / Logical / Vision / Image)
   │
   ▼
Tools
   (Browser / FileSystem / Terminal / Memory)
   │
   ▼
VerifierAgent
   │  checks correctness, completeness, security, quality
   ▼
Response to User
   │
   ▼
MemoryAgent
   │  extracts useful information, stores into the LLM Wiki
```

## Agents

**ClassifierAgent** — Analyzes incoming requests and decides which agent should handle them, whether planning is needed, whether memory retrieval is needed, and whether verification is required. Outputs structured routing decisions, e.g.:

```json
{
  "agent": "coding",
  "planning_required": true,
  "memory_required": true,
  "verification_required": true
}
```

**PlannerAgent** — Generates step-by-step execution plans for complex tasks (e.g. "Build a Flask API with JWT authentication" → project structure → config → models → auth → routes → tests → security review). Simple requests bypass planning.

**ChatAgent** — General conversation: question answering, explanations, discussions, knowledge retrieval.

**LogicalAgent** — Reasoning-heavy tasks: problem solving, analysis, decision making, multi-step reasoning.

**CodingAgent** — Software engineering: generating, refactoring, and debugging code, running tools, reading/modifying files, executing terminal commands. Makes heavy use of the FileSystem, Terminal, and Browser tools.

**VisionAgent** — Image analysis: OCR, visual understanding, image description, UI analysis, screenshot analysis.

**ImageAgent** — Image generation from prompts: concept art, diagrams, visual assets.

**VerifierAgent** — Reviews agent output before it reaches the user, checking correctness, completeness, security, logic, and code quality. Approves or requests revision.

**MemoryAgent** — Processes conversations after the fact: extracts facts, updates the user profile, tracks interests, records preferences, and saves relevant chat history.

## Tools

**Browser Tool** — Internet access: search the web, read pages, collect information. Used by ChatAgent, LogicalAgent, and CodingAgent.

**FileSystem Tool** — Read, create, edit, and delete local files. Used heavily by CodingAgent.

**Terminal Tool** — Run scripts, execute shell commands, manage projects. Used heavily by CodingAgent.

**Memory Tool** — Search and retrieve from the LLM Wiki: facts, profile, interests, skills, and chat history.

## Memory System (LLM Wiki)

The memory system is markdown-based — no database required initially. Everything is stored as structured markdown files under `memory/`.

| File | Stores |
|---|---|
| `facts/facts.md` | Objective information (e.g. "User uses Ubuntu", "User owns RTX 4050") |
| `profile/profile.md` | Identity and preferences (e.g. "Computer Science student", "Interested in AI and Robotics") |
| `interest/interest.md` | Long-term interests (e.g. LangChain, LangGraph, Robotics) |
| `skills/skills.md` | Learned preferences and workflows (e.g. "Prefers FastAPI over Flask", "Prefers complete code over snippets") |
| `chat/chat.md` | Important conversation summaries — not every message, only useful context |

**Memory vs. Knowledge:** memory is information about the user; knowledge is information about the world. These are kept as separate systems.

## Roadmap

**Knowledge system** — a separate, future knowledge base for world information, structured as:

```
knowledge/
├── articles/
├── summaries/
├── graph/
└── index/
```

**Autonomous learning** — the system will eventually learn topics automatically based on tracked user interests:

```
Interests → Search Internet → Collect Content → Summarize → Deduplicate → Store Knowledge
```

For example, given the interest "LangGraph," the system would search for recent updates, read articles, summarize findings, and store the result locally — building a continuously growing personal knowledge base.

**Other planned additions:** LangGraph, vector search, knowledge graphs, embeddings, RAG retrieval.

## Tech Stack

- Python
- LangChain
- Ollama (local LLMs)
- Markdown-based memory
- Local filesystem storage

## Design Philosophy

1. Fully local whenever possible.
2. Modular agent architecture.
3. Clear separation of memory and knowledge.
4. Verification before any response reaches the user.
5. Long-term learning through memory.
6. Extensible tool ecosystem.
7. A personal AI assistant that improves over time, not a static chatbot.
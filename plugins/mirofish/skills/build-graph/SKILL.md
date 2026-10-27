---
name: build-graph
description: "Extract a MiroFish social-actor ontology, directed knowledge graph, and OASIS-style multi-agent persona profiles from seed text or uploaded documents before running a simulation. Use when the user attaches a report, article, policy draft, or story and asks to map stakeholders, build the knowledge graph, design simulation personas, or prepare seed entities."
---

# MiroFish Knowledge Graph & Persona Builder (`build-graph`)

Transform raw documents or scenario descriptions into a structured MiroFish social-actor ontology, conflict graph, and simulation-ready persona cast. Match the user's language (Arabic, English, Chinese, etc.).

## Instructions

### 1. Audit Seed Material
Read all attached files and prompt text. Identify:
- **Factual anchors**: dates, numbers, commitments, constraints, and institutional rules.
- **Core fault lines**: the 2–4 central disagreements or competing incentives driving collective behavior.
- **Information asymmetries**: what insiders know vs. what the public or market initially perceives.

### 2. Construct the Ten-Type Actor Ontology
Every node must be a **real or plausible social actor** capable of speaking, deciding, or influencing others—never an abstract topic or emotion:
- Define **up to 8 scenario-specific concrete `PascalCase` entity types** (such as `CentralBank`, `RetailTrader`, `InvestigativeReporter`, `LaborUnion`, `EnterpriseCustomer`, `PlatformModerator`) with clear, non-overlapping boundaries.
- Append **2 fallback types**: `Person` and `Organization`.
- Define **6 to 10 `UPPER_SNAKE_CASE` directed edge types** (`REGULATES`, `COMPETES_WITH`, `AMPLIFIES`, `CHALLENGES`, `DEPENDS_ON`, `BOYCOTTS`, `ENDORSES`, `REPORTS_ON`).

### 3. Map Concrete Graph Nodes & Directed Edges
Present a concise structured table or diagram of the **8 to 15 highest-leverage entities** and the directed relationships connecting them, noting whether each edge transmits **trust**, **pressure**, **scrutiny**, or **contagion**.

### 4. Generate OASIS-Style Persona Profiles
Produce **6 to 10 simulation-ready archetypes** covering named key actors and broader population cohorts. For each archetype include:
- **Identity & Ontology Type** (`name`, `@handle`, `entity_type`, `population_share`)
- **Behavioral Parameters** (`initial_stance` from `-1.0` to `+1.0`, `conviction` `0.1–0.95`, `influence_weight` `0.5–4.0`, `platform_preference`: `microblog` / `forum` / `balanced`)
- **Persona Psychology** (MBTI, rhetorical style, core incentive, biggest fear, and initial memory of the seed event)

### 5. Hand Off to Simulation
Conclude by asking whether the user wants to:
1. Adjust any stakeholder weights, stances, or missing actors, or
2. Launch the full multi-round swarm simulation immediately (`simulate`).

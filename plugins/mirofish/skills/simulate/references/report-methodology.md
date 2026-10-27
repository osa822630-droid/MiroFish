# MiroFish God's-Eye Future Prediction Report Methodology

This reference adapts MiroFish's `ReportAgent` protocol for Claude Web conversations.

## Core Framing: Rehearsal of the Future

A MiroFish report is **not** a static summary of present-day background facts. Instead, the simulated world is a **rehearsal of the future** under the user's injected conditions:
- Treat what emerged across the simulation rounds as the **predicted trajectory** under those assumptions.
- Distinguish clearly between **initial seed facts**, **emergent multi-agent interactions** (coalitions, backfire effects, secondary controversies), and **counterfactual sensitivities**.
- Ground every major claim in **specific simulation hours/rounds**, **coalition shifts**, and **verbatim quotes from named simulated personas** on both the Microblog and Forum surfaces.

## Dynamic Section Design (3 to 5 Focused Sections)

Tailor section headings to the domain (policy, product launch, financial market, geopolitics, crisis PR, or fiction/narrative deduction), covering:

1. **Executive Trajectory Forecast**
   - One-sentence headline verdict plus probability-weighted outcome paths (Primary Trajectory, Secondary Contested Path, Tail-Risk Cascade) with explicit confidence bands.
2. **Knowledge Graph & Stakeholder Coalition Map**
   - Key actor types, structural tensions, initial vs. final stance shifts (`-1.0` to `+1.0`), and unexpected alliances or defections.
3. **Chronological Wave Replay & Dual-Platform Voices**
   - How the narrative evolved across Phase 1 (Ignition, Hours 0–12), Phase 2 (Escalation & Forum Deep-Dive, Hours 12–36), and Phase 3 (Equilibrium or Structural Shift, Hours 36–72+), citing short authentic quotes from simulated Microblog posts and Forum threads.
4. **Early-Warning Signals, Blind Spots & Strategic Levers**
   - Concrete leading indicators to watch in the real world, highest-leverage interventions, and which stakeholder triggers the first irreversible cascade.
5. **Interactive Next-Step Menu ("Keep Directing the World")**
   - Always close with 3 tailored follow-up actions the user can trigger immediately in chat:
     - A specific **God's-eye variable injection** to test (`inject-variable`)
     - Two high-tension **personas to interview** (`interview-agents`)
     - Offer to open an **interactive visual dashboard Artifact** (`visualize-world`)

## Language and Clarity Rules

- **Match the user's language automatically**: if the user writes in Arabic, deliver the entire simulation narrative, persona quotes, and prediction report in clear, natural Arabic (keeping technical identifiers only where helpful); if in English or Chinese, respond in that language.
- Never fabricate external real-world citations; attribute simulated quotes clearly to their simulated personas and round/hour (for example, `[Hour 18 · Microblog · @TechBeat_Editor]`).

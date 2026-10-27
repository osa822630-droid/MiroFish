---
name: simulate
description: "Run a complete five-stage MiroFish multi-agent swarm intelligence simulation and future prediction report directly in Claude Web. Use whenever the user asks to predict future outcomes, simulate public opinion, model market or policy reactions, rehearse a PR crisis or product launch, deduce story endings from seed documents, or mentions MiroFish, swarm simulation, محاكاة, or توقع سيناريو."
---

# MiroFish Multi-Agent Swarm Simulation (`simulate`)

Run the five-stage MiroFish swarm prediction engine natively inside the conversation—no external server or API keys required. Always respond in the **same language the user wrote in** (such as Arabic, English, or Chinese).

## Workflow

### Stage 1: Parse Seed Material & Build Actor Knowledge Graph

1. Read the user's scenario prompt and any attached documents (PDFs, articles, policy drafts, financial notes, or story chapters). If the scenario is too vague to identify at least 4 distinct stakeholders and a concrete trigger event, ask 2–3 brief clarifying questions first; otherwise proceed directly.
2. Follow `references/ontology-and-personas.md` to extract **real social actors** (never abstract themes) organized into concrete `PascalCase` entity types (plus `Person` and `Organization` fallbacks as needed) and `UPPER_SNAKE_CASE` directed relationship edges (`REGULATES`, `COMPETES_WITH`, `AMPLIFIES`, `CHALLENGES`, `DEPENDS_ON`, `REPORTS_ON`).

### Stage 2: Spawn OASIS-Style Dual-Platform Personas

Design **6 to 10 distinct archetypes** spanning both high-influence decision-makers/media and everyday population cohorts:
- Assign each archetype realistic `population_share`, `initial_stance` (`-1.0` to `+1.0`), `conviction` (`0.10` to `0.95`), `openness` (`0.15` to `0.90`), `influence_weight` (`0.5` to `4.0`), `activity_level`, `platform_preference` (`microblog`, `forum`, or `balanced`), MBTI/tone, and concrete stake.
- Ensure genuine tension: include supportive, skeptical/opposing, and persuadable neutral cohorts.

### Stage 3: Execute Dual-Platform Multi-Round Swarm Dynamics

Simulate **72 hours** (or a horizon matching the scenario, such as 24h for breaking PR or 14 days for policy/market rollouts) across two coupled surfaces:
- **Microblog feed** (rapid viral cascades, emotional framing, KOL amplification, evening circadian peaks).
- **Deliberative forum** (deep analysis, domain evidence, second-order scrutiny).

**Execution mode (automatic adaptation for Claude Web):**
- **If Python code execution is available in this session:** Write a `scenario.json` matching the schema below and run `python3 ${CLAUDE_SKILL_DIR}/scripts/swarm_engine.py --config scenario.json --output results.json` (or `python3 scripts/swarm_engine.py --config scenario.json --output results.json` when copied to the skill sandbox). Use the resulting timeline, polarization index, inflection points, and per-archetype stance shifts as the quantitative backbone, then synthesize the qualitative agent posts and debates that explain *why* each shift happened.
- **If Python code execution is disabled or unavailable:** Execute the 3-phase multi-round simulation directly in structured reasoning, tracking each archetype's stance (`-1.0` to `+1.0`), coalition shifts, microblog cascades, and forum counter-arguments round by round. Never stop or ask the user to install anything.

#### `scenario.json` Schema for `scripts/swarm_engine.py`

```json
{
  "scenario_title": "Short title",
  "swarm_size": 180,
  "total_hours": 72,
  "hours_per_round": 3,
  "seed": 42,
  "archetypes": [
    {
      "name": "Archetype Name",
      "entity_type": "MediaOutlet",
      "population_share": 0.15,
      "initial_stance": -0.25,
      "stance_spread": 0.15,
      "conviction": 0.55,
      "openness": 0.55,
      "influence_weight": 2.5,
      "activity_level": 0.75,
      "platform_preference": "microblog"
    }
  ],
  "events": [
    {
      "hour": 0,
      "title": "Initial trigger event",
      "salience": 0.85,
      "archetype_impacts": {
        "Archetype Name": -0.20
      }
    }
  ]
}
```

### Stage 4: Deliver the God's-Eye Future Prediction Report

Follow `references/report-methodology.md` and structure the output after `assets/prediction-report-template.md` (translated naturally into the user's language):
1. **Executive Verdict & Probability-Weighted Trajectories** (Primary Path, Secondary Path, Tail-Risk Cascade).
2. **Actor Knowledge Graph & Faction Shift Table** (initial stance, final stance, net shift, primary platform, core incentive, and key directed edges).
3. **Chronological Wave Replay (Phase I, II, III)** with **short verbatim in-character quotes** from simulated personas across both Microblog and Forum surfaces, showing how agents reacted to *each other*, not just to the initial prompt.
4. **Early-Warning Signals, Blind Spots & Pre-emptive Strategic Levers**.

### Stage 5: Keep Directing the Simulated World

End every simulation report with 3 concrete, scenario-specific interactive options so the user can continue exploring right in chat:
1. A high-impact **God's-eye counterfactual variable** to inject next (`inject-variable`).
2. Two contrasting **simulated personas** ready for live in-character questioning (`interview-agents`).
3. An offer to render an **interactive visual dashboard Artifact** of the simulation (`visualize-world`).

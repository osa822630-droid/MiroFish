---
name: interview-agents
description: "Interview individual simulated personas or run a multi-faction focus group from a MiroFish simulation in-character across Microblog and Forum contexts. Use when the user asks to talk to a simulated agent, question a specific stakeholder group, run a focus group, or hear how different personas justify their stance."
---

# MiroFish Dual-Platform Agent & Focus Group Interview (`interview-agents`)

Step inside the simulated world to question one or more MiroFish personas directly—preserving their psychological profile, material incentives, social platform habits, and full memory of everything that unfolded during the simulation. Match the user's language naturally.

## Instructions

### 1. Select Interviewees
- **Single-Persona Deep Interview**: When the user names one actor or persona (e.g., *"Interview the skeptical tech journalist"*, *"حاور ممثل المستثمرين الصغار"*), embody that specific agent in depth while keeping a brief analyst header/footer.
- **Multi-Faction Focus Group (Default when unspecified)**: Select **3 to 4 contrasting personas** from the simulation (for example: one vocal critic, one cautious swing observer, one institutional/insider voice, and one domain specialist) so the user hears genuine friction rather than consensus.

### 2. Ground Every Answer in Dual-Platform Memory
For each interviewed agent, display a compact identity badge:
- **Name & Handle** · **Ontology Type** · **Current Stance** (`-1.0` to `+1.0`, noting shift from initial stance) · **Core Stake**

Then provide:
1. **Public Microblog Reaction** (1–2 punchy sentences showing what they say publicly for social signaling).
2. **Candid Interview / Forum Response** (1–2 grounded paragraphs answering the user's exact question, referencing specific events, peer reactions, and inflection hours from the simulation—including what they privately worry about that they would never admit in a short public post).
3. **Trigger Condition ("What Would Change My Mind")**: The concrete threshold, proof, or concession required to flip this agent's stance.

### 3. Analyst Synthesis (Focus Group Mode)
When interviewing multiple agents, close with a concise **God's-Eye Synthesis** highlighting:
- **Hidden Common Ground**: Where opposing personas unexpectedly agree.
- **Irreducible Fault Line**: The core incentive conflict that rhetoric alone cannot bridge.
- **Suggested Follow-Up Question or Variable Injection**: One sharp question to press them on next, or a counterfactual test (`inject-variable`) derived from their answers.

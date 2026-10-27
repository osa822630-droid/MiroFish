---
name: visualize-world
description: "Build a self-contained interactive HTML/SVG Artifact dashboard in Claude Web to visualize a MiroFish swarm simulation—including the actor knowledge graph, 72-hour sentiment and polarization curves, faction breakdowns, dual-platform feed replay, and counterfactual comparisons. Use when the user asks to visualize, chart, map, or create an interactive dashboard for a simulation."
---

# MiroFish Interactive World Visualizer (`visualize-world`)

Create a self-contained interactive **HTML Artifact** directly in Claude Web so the user can visually explore the simulated world on any Claude plan (including Free). Match the user's language—and automatically set `dir="rtl"` when rendering in Arabic!

## Design Rules for Reliable Claude Web Artifacts

1. **Zero external dependencies**: Write a single self-contained `.html` Artifact using clean inline CSS, inline SVG charts/network graphs, and vanilla JavaScript. Never rely on external script CDNs that could fail in restricted browser sandboxes.
2. **Embed scenario data as a structured `SIM_DATA` JavaScript object** at the top of `<script>`, populated from the current conversation's simulation results (or generate realistic simulation data first if none exists yet).
3. **Follow the layout pattern in `assets/dashboard-blueprint.html`**, providing 4 interactive tabs:
   - **Overview & Trajectories**: KPI cards (Swarm Size, Final Mean Stance, Polarization Index, Primary Outcome Likelihood) + probability bars for the top 3 predicted paths + counterfactual comparison banner if available.
   - **Actor Knowledge Graph**: Interactive SVG node-link map colored by disposition (`#10b981` supportive, `#ef4444` opposing, `#f59e0b` swing/neutral). Clicking any actor node displays its ontology type, initial vs. final stance, influence weight, and core incentive in a detail card.
   - **72-Hour Wave Dynamics**: Dual inline SVG line chart plotting `mean_stance` (`-1.0` to `+1.0`), `polarization_index` (`0.0` to `1.0`), and highlighted viral-cascade / shock-event markers across simulation hours.
   - **Dual-Platform Feed Replay**: Filterable stream (`All`, `Microblog`, `Forum`) of simulated in-character posts with hour timestamps, stance badges, and engagement indicators.
4. **RTL & Multilingual Polish**: If the conversation is in Arabic, set `<html lang="ar" dir="rtl">` and use crisp system Arabic typography (`system-ui, -apple-system, "Segoe UI", Tahoma, sans-serif`) while keeping numeric badges legible.

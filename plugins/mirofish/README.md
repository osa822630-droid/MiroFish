# MiroFish Swarm Intelligence Plugin for Claude Web

MiroFish Swarm Intelligence brings the five-stage MiroFish multi-agent prediction workflow directly into Claude Web conversations on claude.ai, as well as Claude Desktop, Cowork, and Claude Code. No local server, terminal setup, or third-party cloud credentials are required.

Upload seed materials (news articles, policy drafts, market briefs, product plans, research reports, or fiction manuscripts) or describe any scenario in natural language—in Arabic, English, Chinese, or any language—and Claude constructs a parallel digital world of interacting personas to rehearse future outcomes before they happen.

## Included Skills

- **`simulate`**: Run the complete five-stage MiroFish swarm prediction pipeline—ontology and knowledge graph extraction, OASIS-style dual-platform persona generation, multi-round social simulation across fast-viral microblog feeds and deliberative forum threads, and a God's-eye future prediction report.
- **`build-graph`**: Extract social-actor ontologies (eight concrete entity types plus `Person` and `Organization` fallbacks), directed relationship edges, conflict lines, and ready-to-run agent profiles from uploaded documents or pasted seed text.
- **`inject-variable`**: Inject a shock event, policy adjustment, crisis response, or counterfactual change from a God's-eye view at any simulation hour and compare the branched trajectory against the baseline forecast.
- **`interview-agents`**: Conduct in-character interviews or multi-faction focus groups with simulated personas across microblog and forum contexts, grounded in their post-simulation memory and stance evolution.
- **`visualize-world`**: Render a self-contained interactive HTML dashboard Artifact inside Claude Web to explore the actor knowledge graph, 72-hour sentiment and polarization waves, faction coalitions, platform feed highlights, and early-warning risk signals.

## How to Use on Claude Web

1. Open **Customize > Plugins** in the left sidebar on claude.ai.
2. Select **Add > Add marketplace**, enter `osa822630-droid/MiroFish`, and click **Sync**.
3. Click **Add** next to **MiroFish Swarm Intelligence**.
4. Start any chat on claude.ai, attach a document or describe a scenario, and either speak naturally or type `/` (or click `+`) to pick any MiroFish skill.

When Claude Web's built-in Python code execution capability is enabled, the `simulate` skill automatically runs its bundled pure-Python standard-library swarm dynamics script (`scripts/swarm_engine.py`) to compute quantitative opinion shifts, circadian activity curves, polarization indices, and viral cascade tipping points alongside qualitative multi-agent dialogue. When code execution is turned off, every skill operates seamlessly through structured multi-round reasoning in chat.

## Data and Privacy

This plugin runs entirely inside your Claude conversation and Claude's built-in code execution sandbox. It includes only Markdown instructions, HTML templates, and a standalone Python standard-library simulation script. It makes zero external network requests, connects to no external servers, reads no machine credentials, and stores no data outside your Claude session.

---
name: inject-variable
description: "Inject a God's-eye counterfactual variable, shock event, policy tweak, or crisis response into a MiroFish simulation and compare the branched trajectory against the baseline forecast. Use whenever the user asks 'What if...', 'ماذا لو...', tests an intervention at a specific hour, changes a scenario variable, or stress-tests an alternative strategy."
---

# MiroFish God's-Eye Variable Injection (`inject-variable`)

Branch an existing (or newly described) MiroFish simulation from a **God's-eye perspective** by injecting one or more shock variables at a specific simulation hour and comparing the counterfactual world against the baseline trajectory. Always respond in the user's language.

## Instructions

### 1. Specify the Injected Variable Precisely
Extract from the user's request:
- **Injection Timing**: At what simulation hour/stage does the intervention hit (e.g., `Hour 0` pre-emptive design change, `Hour 12` rapid crisis response, or `Hour 36` delayed regulatory intervention)?
- **Direct Stakeholder Impacts**: Which archetypes have their material incentives updated positively or negatively (`-0.8` to `+0.8`), and how high is the event's `salience` (`0.1` to `1.0`)?
- **Second-Order Signal**: Does the move project credibility and transparency, or panic and concession?

### 2. Compute Baseline vs. Counterfactual Divergence
- **If Python code execution is available**, populate `"counterfactual_events"` in a scenario JSON configuration and run `python3 ${CLAUDE_SKILL_DIR}/scripts/swarm_engine.py --config scenario.json --output counterfactual_results.json` (or `python3 scripts/swarm_engine.py --config scenario.json --output counterfactual_results.json` inside the skill sandbox) to compute exact baseline vs. branched stance, polarization, and coalition deltas.
- **If running in pure conversational mode**, trace round-by-round how the injected variable alters:
  1. Immediate **Microblog** framing (does it defuse or inflame viral momentum?),
  2. Subsequent **Forum** scrutiny (do domain analysts validate the move or expose loopholes?),
  3. Coalition alignments (which swing cohort flips first, and who remains entrenched?).

### 3. Deliver the Counterfactual Comparison Report
Present a crisp side-by-side comparison:

| Metric / Dimension | Baseline World | Counterfactual Branch | Net Delta & Verdict |
| --- | --- | --- | --- |
| **Dominant Outcome** | [Baseline path] | [Branched path] | [Improved / Worsened / Shifted] |
| **Mean Swarm Stance** | `[-1..+1]` | `[-1..+1]` | `[+/- delta]` |
| **Polarization Index** | `[0..1]` | `[0..1]` | `[+/- delta]` |
| **Supportive / Opposing Share** | `[% / %]` | `[% / %]` | `[Swing summary]` |
| **Key Flip Cohort** | [Stance] | [New stance] | [Why they moved] |

Include **2–3 short verbatim quotes** showing how key simulated personas react right after the variable hits on Microblog and Forum surfaces, plus **1 unintended side-effect or second-order risk** introduced by the intervention.

### 4. Suggest Next Experiment
Offer 2 follow-up experiments: testing **earlier vs. later timing** of the same intervention, or **interviewing the swing cohort** (`interview-agents`) to hear why they flipped.

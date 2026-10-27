# MiroFish Ontology and Dual-Platform Persona Design

This reference defines how MiroFish transforms raw seed materials into an actor knowledge graph and an OASIS-style social agent cast.

## 1. Social-Actor Ontology Rules

Every entity in a MiroFish simulation must be a **real or plausible social actor** capable of speaking, deciding, amplifying, or reacting in public or institutional arenas.

### Allowed Entity Categories
- Concrete individuals (executives, policymakers, whistleblowers, domain experts, creators, everyday citizens)
- Companies and commercial brands (including official corporate accounts)
- Institutions and organizations (universities, associations, unions, NGOs, research labs)
- Government ministries, courts, central banks, and regulators
- Media outlets, investigative journalists, and independent commentary channels
- Grassroots collectives (customer groups, investor cohorts, alumni networks, fan communities)

### Prohibited Entity Categories
- Abstract nouns or themes (for example, "Inflation", "Public Anger", "AI Ethics")
- Pure stances without an actor identity (for example, "Supporters", "Critics")

### Ten-Type Hierarchy
When mapping a complex scenario, define **up to 10 entity types**:
- **Up to 8 scenario-specific concrete types** with non-overlapping boundaries (such as `Regulator`, `RetailInvestor`, `TechJournalist`, `EnterpriseBuyer`, `CompetitorBrand`, `CoreDeveloper`)
- **2 mandatory fallback types** placed last:
  - `Person`: fallback for any individual who does not fit a specialized individual type
  - `Organization`: fallback for any institution or collective that does not fit a specialized organization type

### Directed Relationship Edges
Define **6 to 10 relationship types** in `UPPER_SNAKE_CASE` connecting explicit source and target actors, such as:
- `REGULATES`, `COMPETES_WITH`, `AMPLIFIES`, `CHALLENGES`, `DEPENDS_ON`, `REPORTS_ON`, `BOYCOTTS`, `ENDORSES`, `ADVISES`

## 2. OASIS-Style Dual-Platform Persona Schema

Generate **6 to 10 distinct archetypes** (representing both named high-leverage actors and broader population cohorts) with conflicting incentives, asymmetric information, and distinct communication habits:

| Field | Range / Format | Role in Simulation |
| --- | --- | --- |
| `name` | Distinct actor or cohort title | Identifies the voice in feeds, tables, and interviews |
| `entity_type` | PascalCase ontology type | Links the persona back to the knowledge graph |
| `population_share` | `0.02` to `0.50` | Cohort weight when expanding into a 100–300 agent swarm |
| `initial_stance` | `-1.0` (strongly opposing) to `+1.0` (strongly supportive) | Starting disposition before peer contagion |
| `conviction` | `0.10` (malleable) to `0.95` (ideologically anchored) | Resistance to persuasion and social pressure |
| `openness` | `0.15` (echo-chamber) to `0.90` (broadly receptive) | Bounded-confidence threshold for peer persuasion vs. backfire |
| `influence_weight` | `0.5` (ordinary user) to `4.0` (major authority / media) | Reach and visibility across social feeds |
| `activity_level` | `0.15` to `0.95` | Posting frequency across circadian hours |
| `platform_preference` | `microblog`, `forum`, or `balanced` | Primary arena where this persona shapes narratives |
| `mbti_and_tone` | MBTI + rhetorical style | Keeps qualitative quotes authentic and non-uniform |
| `core_incentive` | Concrete stake (financial, reputational, institutional) | Explains why the persona reacts the way it does |

## 3. Dual-Platform Interaction Mechanics

MiroFish runs two coupled social surfaces in parallel because real-world narratives split across fast emotional feeds and slower analytical communities:

1. **Microblog Surface (X / Twitter / Weibo style)**
   - Weighted toward recency, emotional intensity, quote-amplification, and high-follower opinion leaders.
   - Ignites **viral cascades** during evening peak hours (`19:00–22:00`) or right after high-salience shock events.
   - Prone to frame hijacking, slogans, and polarization spikes when opposing camps collide outside their confidence bounds.

2. **Deliberative Forum Surface (Reddit / HN / Niche Community style)**
   - Weighted toward detailed evidence, domain credibility, upvote/downvote filtering, and technical or financial scrutiny.
   - Often surfaces second-order risks, workarounds, contractual details, or fact-checks 12–36 hours after the initial microblog wave, which then feed back into mainstream media coverage.

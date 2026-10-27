#!/usr/bin/env python3
"""
MiroFish Standalone Swarm Dynamics Engine for Claude Web.

Pure Python 3 standard-library multi-agent social simulation engine modeled on
MiroFish's dual-platform (Microblog + Forum) and circadian interaction design.
Runs offline inside Claude's built-in Python sandbox with zero external packages
and zero network requests.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


CIRCADIAN_MULTIPLIERS: Dict[int, float] = {
    0: 0.08, 1: 0.06, 2: 0.05, 3: 0.05, 4: 0.06, 5: 0.12,
    6: 0.35, 7: 0.48, 8: 0.62,
    9: 0.75, 10: 0.80, 11: 0.78, 12: 0.85, 13: 0.75, 14: 0.72,
    15: 0.74, 16: 0.78, 17: 0.82, 18: 0.95,
    19: 1.35, 20: 1.50, 21: 1.55, 22: 1.38,
    23: 0.55,
}


def clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


@dataclass
class SimAgent:
    agent_id: int
    archetype: str
    entity_type: str
    stance: float
    initial_stance: float
    anchor_stance: float
    conviction: float
    influence: float
    activity: float
    confidence_bound: float
    microblog_affinity: float
    forum_affinity: float
    memory_trace: List[str] = field(default_factory=list)


def build_swarm(config: Dict[str, Any], rng: random.Random) -> List[SimAgent]:
    """Expand archetype definitions into an interacting multi-agent swarm."""
    target_total = int(config.get("swarm_size", 180))
    target_total = max(24, min(600, target_total))
    archetypes = config.get("archetypes", [])
    if not archetypes:
        raise ValueError("Configuration must contain a non-empty 'archetypes' list.")

    raw_shares = [max(0.02, float(a.get("population_share", 1.0))) for a in archetypes]
    share_sum = sum(raw_shares)
    counts = [max(2, round(target_total * s / share_sum)) for s in raw_shares]

    agents: List[SimAgent] = []
    next_id = 1
    for arch, count in zip(archetypes, counts):
        name = str(arch.get("name", f"Group-{next_id}"))
        entity_type = str(arch.get("entity_type", "Person"))
        base_stance = clamp(float(arch.get("initial_stance", 0.0)))
        spread = max(0.03, min(0.45, float(arch.get("stance_spread", 0.16))))
        conviction = clamp(float(arch.get("conviction", 0.50)), 0.08, 0.95)
        influence = clamp(float(arch.get("influence_weight", 1.0)), 0.2, 5.0)
        activity = clamp(float(arch.get("activity_level", 0.55)), 0.1, 1.0)
        conf_bound = clamp(float(arch.get("openness", 0.55)), 0.15, 0.95)
        platform_pref = str(arch.get("platform_preference", "balanced")).lower()

        if platform_pref in ("microblog", "twitter", "x"):
            mb_aff, fr_aff = 0.85, 0.35
        elif platform_pref in ("forum", "reddit"):
            mb_aff, fr_aff = 0.35, 0.85
        else:
            mb_aff, fr_aff = 0.65, 0.65

        for idx in range(count):
            # First agent of high-influence archetypes acts as key opinion leader / official voice
            is_lead = idx == 0 and influence >= 1.5
            stance = clamp(base_stance + (0.0 if is_lead else rng.gauss(0.0, spread)))
            agent_influence = influence * (1.8 if is_lead else rng.uniform(0.75, 1.25))
            agents.append(
                SimAgent(
                    agent_id=next_id,
                    archetype=name,
                    entity_type=entity_type,
                    stance=stance,
                    initial_stance=stance,
                    anchor_stance=stance,
                    conviction=clamp(conviction + rng.uniform(-0.08, 0.08), 0.05, 0.96),
                    influence=agent_influence,
                    activity=clamp(activity + rng.uniform(-0.12, 0.12), 0.08, 1.0),
                    confidence_bound=conf_bound,
                    microblog_affinity=mb_aff,
                    forum_affinity=fr_aff,
                )
            )
            next_id += 1

    return agents


def disposition_label(stance: float) -> str:
    if stance >= 0.25:
        return "supportive"
    if stance <= -0.25:
        return "opposing"
    return "neutral_or_ambivalent"


def compute_polarization(stances: List[float]) -> float:
    """Normalized polarization index in [0, 1] combining spread and bimodal split."""
    if len(stances) < 2:
        return 0.0
    stdev = statistics.pstdev(stances)
    pos = [s for s in stances if s >= 0.25]
    neg = [s for s in stances if s <= -0.25]
    n = len(stances)
    bimodal_balance = 4.0 * (len(pos) / n) * (len(neg) / n)
    raw = 0.55 * min(1.0, stdev / 0.65) + 0.45 * bimodal_balance
    return round(clamp(raw, 0.0, 1.0), 4)


def apply_events_at_hour(
    agents: List[SimAgent],
    events: List[Dict[str, Any]],
    window_start: int,
    window_end: int,
    rng: random.Random,
) -> List[str]:
    """Inject scheduled or counterfactual events falling in [window_start, window_end)."""
    triggered_titles: List[str] = []
    for event in events:
        ev_hour = int(event.get("hour", 0))
        if not (window_start <= ev_hour < window_end):
            continue
        title = str(event.get("title", f"Event@{ev_hour}h"))
        triggered_titles.append(title)
        salience = clamp(float(event.get("salience", 0.7)), 0.1, 1.0)
        global_shift = clamp(float(event.get("global_shift", 0.0)), -0.8, 0.8)
        impacts: Dict[str, Any] = event.get("archetype_impacts", {}) or {}

        for agent in agents:
            delta = float(impacts.get(agent.archetype, global_shift))
            if abs(delta) < 1e-6:
                continue
            susceptibility = (1.0 - 0.45 * agent.conviction) * salience
            noise = rng.gauss(0.0, 0.03 * salience)
            applied = delta * susceptibility + noise
            agent.stance = clamp(agent.stance + applied)
            agent.anchor_stance = clamp(agent.anchor_stance + 0.70 * applied)
            agent.memory_trace.append(f"h{ev_hour}:{title}")

    return triggered_titles


def run_simulation(config: Dict[str, Any], extra_events: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    seed = int(config.get("seed", 42))
    rng = random.Random(seed)
    agents = build_swarm(config, rng)

    total_hours = max(6, min(336, int(config.get("total_hours", 72))))
    hours_per_round = max(1, min(24, int(config.get("hours_per_round", 3))))
    start_hour_of_day = int(config.get("start_hour_of_day", 9)) % 24
    viral_threshold = float(config.get("viral_threshold", 0.34))

    all_events = list(config.get("events", []))
    if extra_events:
        all_events.extend(extra_events)

    timeline: List[Dict[str, Any]] = []
    inflections: List[Dict[str, Any]] = []
    prev_mean: Optional[float] = None
    prev_pol: Optional[float] = None

    num_rounds = math.ceil(total_hours / hours_per_round)
    for round_idx in range(num_rounds):
        sim_hour = round_idx * hours_per_round
        next_hour = min(total_hours, sim_hour + hours_per_round)
        clock_hour = (start_hour_of_day + sim_hour) % 24
        circadian = CIRCADIAN_MULTIPLIERS.get(clock_hour, 0.7)

        triggered = apply_events_at_hour(agents, all_events, sim_hour, next_hour, rng)

        # Select active microblog & forum speakers this round
        mb_posts: List[Tuple[float, float]] = []  # (stance, weight)
        fr_posts: List[Tuple[float, float]] = []

        for agent in agents:
            act_prob = clamp(agent.activity * circadian, 0.03, 0.98)
            if rng.random() < act_prob * agent.microblog_affinity:
                # Microblog rewards emotional extremity + influence
                extremity_boost = 1.0 + 0.65 * abs(agent.stance)
                mb_posts.append((agent.stance, agent.influence * extremity_boost))
            if rng.random() < act_prob * agent.forum_affinity:
                # Forum weights credibility and substantive moderation
                moderation_boost = 1.0 + 0.30 * (1.0 - abs(agent.stance) * 0.4)
                fr_posts.append((agent.stance, agent.influence * moderation_boost))

        if mb_posts:
            mb_total_w = sum(w for _, w in mb_posts)
            mb_signal = sum(s * w for s, w in mb_posts) / mb_total_w
            mb_intensity = mb_total_w / max(1.0, len(agents))
        else:
            mb_signal = statistics.mean(a.stance for a in agents)
            mb_intensity = 0.05

        if fr_posts:
            fr_total_w = sum(w for _, w in fr_posts)
            fr_signal = sum(s * w for s, w in fr_posts) / fr_total_w
        else:
            fr_signal = statistics.mean(a.stance for a in agents)

        viral_active = mb_intensity >= viral_threshold or bool(triggered and abs(mb_signal) >= 0.28)
        cascade_mult = 1.45 if viral_active else 1.0

        # Update agent stances via bounded-confidence peer interaction + platform signals
        new_stances: List[float] = []
        n_agents = len(agents)
        for agent in agents:
            peers = rng.sample(agents, k=min(5, n_agents))
            peer_pull = 0.0
            for peer in peers:
                if peer.agent_id == agent.agent_id:
                    continue
                diff = peer.stance - agent.stance
                if abs(diff) <= agent.confidence_bound:
                    peer_pull += 0.045 * diff * min(2.2, peer.influence)
                elif abs(diff) > 1.25 and viral_active:
                    # Backfire / entrenched polarization under intense viral conflict
                    peer_pull -= 0.012 * math.copysign(1.0, diff)

            mb_diff = mb_signal - agent.stance
            if abs(mb_diff) <= 1.35 * agent.confidence_bound:
                mb_effect = 0.032 * agent.microblog_affinity * cascade_mult * mb_diff
            elif viral_active:
                mb_effect = -0.010 * agent.microblog_affinity * math.copysign(1.0, mb_diff)
            else:
                mb_effect = 0.006 * agent.microblog_affinity * mb_diff

            fr_diff = fr_signal - agent.stance
            if abs(fr_diff) <= 1.55 * agent.confidence_bound:
                fr_effect = 0.028 * agent.forum_affinity * fr_diff
            else:
                fr_effect = 0.005 * agent.forum_affinity * fr_diff

            platform_pull = mb_effect + fr_effect
            anchor_pull = 0.065 * agent.conviction * (agent.anchor_stance - agent.stance)
            step = (peer_pull + platform_pull) * (1.0 - 0.60 * agent.conviction) + anchor_pull
            new_stances.append(clamp(agent.stance + step))

        for agent, updated in zip(agents, new_stances):
            agent.stance = updated

        stances = [a.stance for a in agents]
        mean_stance = round(statistics.mean(stances), 4)
        pol_index = compute_polarization(stances)
        consensus_index = round(clamp(1.0 - pol_index, 0.0, 1.0), 4)
        sup_share = round(sum(1 for s in stances if s >= 0.25) / n_agents, 4)
        opp_share = round(sum(1 for s in stances if s <= -0.25) / n_agents, 4)
        neu_share = round(max(0.0, 1.0 - sup_share - opp_share), 4)

        point = {
            "round": round_idx + 1,
            "hour": next_hour,
            "clock_hour": clock_hour,
            "mean_stance": mean_stance,
            "polarization_index": pol_index,
            "consensus_index": consensus_index,
            "supportive_share": sup_share,
            "opposing_share": opp_share,
            "neutral_share": neu_share,
            "microblog_signal": round(mb_signal, 4),
            "forum_signal": round(fr_signal, 4),
            "viral_cascade": viral_active,
            "triggered_events": triggered,
        }
        timeline.append(point)

        stance_jump = abs(mean_stance - prev_mean) if prev_mean is not None else 0.0
        pol_jump = (pol_index - prev_pol) if prev_pol is not None else 0.0
        if triggered or stance_jump >= 0.07 or pol_jump >= 0.06 or (viral_active and round_idx in (0, 1, 2)):
            reasons = []
            if triggered:
                reasons.append(f"Events: {', '.join(triggered)}")
            if stance_jump >= 0.07:
                reasons.append(f"Rapid sentiment shift ({mean_stance - (prev_mean or 0.0):+.3f})")
            if pol_jump >= 0.06:
                reasons.append(f"Polarization surge (+{pol_jump:.3f})")
            if viral_active:
                reasons.append("Microblog viral cascade active")
            inflections.append(
                {
                    "hour": next_hour,
                    "mean_stance": mean_stance,
                    "polarization_index": pol_index,
                    "reasons": reasons,
                }
            )

        prev_mean = mean_stance
        prev_pol = pol_index

    # Summarize per-archetype outcomes
    by_arch: Dict[str, List[SimAgent]] = {}
    for agent in agents:
        by_arch.setdefault(agent.archetype, []).append(agent)

    archetype_outcomes: List[Dict[str, Any]] = []
    for arch_def in config.get("archetypes", []):
        name = str(arch_def.get("name"))
        group = by_arch.get(name, [])
        if not group:
            continue
        init_avg = statistics.mean(a.initial_stance for a in group)
        final_avg = statistics.mean(a.stance for a in group)
        archetype_outcomes.append(
            {
                "name": name,
                "entity_type": group[0].entity_type,
                "agent_count": len(group),
                "initial_stance": round(init_avg, 4),
                "final_stance": round(final_avg, 4),
                "net_shift": round(final_avg - init_avg, 4),
                "final_disposition": disposition_label(final_avg),
                "platform_preference": str(arch_def.get("platform_preference", "balanced")),
                "influence_weight": float(arch_def.get("influence_weight", 1.0)),
            }
        )

    final_point = timeline[-1]
    return {
        "scenario_title": str(config.get("scenario_title", "MiroFish Swarm Simulation")),
        "swarm_size": len(agents),
        "total_hours": total_hours,
        "hours_per_round": hours_per_round,
        "final_summary": {
            "mean_stance": final_point["mean_stance"],
            "overall_disposition": disposition_label(final_point["mean_stance"]),
            "polarization_index": final_point["polarization_index"],
            "consensus_index": final_point["consensus_index"],
            "supportive_share": final_point["supportive_share"],
            "opposing_share": final_point["opposing_share"],
            "neutral_share": final_point["neutral_share"],
        },
        "archetype_outcomes": archetype_outcomes,
        "inflection_points": inflections[:8],
        "timeline": timeline,
    }


def run_with_optional_counterfactual(config: Dict[str, Any]) -> Dict[str, Any]:
    baseline = run_simulation(config)
    cf_events = config.get("counterfactual_events")
    if not cf_events:
        return baseline

    branched = run_simulation(config, extra_events=cf_events)
    base_sum = baseline["final_summary"]
    cf_sum = branched["final_summary"]
    baseline["counterfactual_comparison"] = {
        "injected_events": cf_events,
        "branched_final_summary": cf_sum,
        "deltas": {
            "mean_stance_delta": round(cf_sum["mean_stance"] - base_sum["mean_stance"], 4),
            "polarization_delta": round(cf_sum["polarization_index"] - base_sum["polarization_index"], 4),
            "supportive_share_delta": round(cf_sum["supportive_share"] - base_sum["supportive_share"], 4),
            "opposing_share_delta": round(cf_sum["opposing_share"] - base_sum["opposing_share"], 4),
        },
        "branched_archetype_outcomes": branched["archetype_outcomes"],
        "branched_timeline": branched["timeline"],
    }
    return baseline


SAMPLE_CONFIG: Dict[str, Any] = {
    "scenario_title": "Subscription Pricing Change Rehearsal",
    "swarm_size": 120,
    "total_hours": 72,
    "hours_per_round": 6,
    "seed": 42,
    "archetypes": [
        {
            "name": "Power Users",
            "entity_type": "CustomerSegment",
            "population_share": 0.25,
            "initial_stance": -0.35,
            "conviction": 0.65,
            "influence_weight": 1.8,
            "activity_level": 0.80,
            "platform_preference": "forum",
        },
        {
            "name": "Casual Users",
            "entity_type": "Person",
            "population_share": 0.45,
            "initial_stance": -0.15,
            "conviction": 0.35,
            "influence_weight": 0.8,
            "activity_level": 0.45,
            "platform_preference": "microblog",
        },
        {
            "name": "Tech Journalists",
            "entity_type": "MediaOutlet",
            "population_share": 0.10,
            "initial_stance": -0.20,
            "conviction": 0.55,
            "influence_weight": 2.8,
            "activity_level": 0.75,
            "platform_preference": "microblog",
        },
        {
            "name": "Enterprise Buyers",
            "entity_type": "Company",
            "population_share": 0.20,
            "initial_stance": 0.30,
            "conviction": 0.60,
            "influence_weight": 1.4,
            "activity_level": 0.40,
            "platform_preference": "forum",
        },
    ],
    "events": [
        {
            "hour": 0,
            "title": "Announcement of 30% price increase with new AI tier",
            "salience": 0.85,
            "archetype_impacts": {
                "Power Users": -0.25,
                "Casual Users": -0.20,
                "Tech Journalists": -0.15,
                "Enterprise Buyers": 0.15,
            },
        }
    ],
    "counterfactual_events": [
        {
            "hour": 18,
            "title": "CEO announces 12-month grandfathering for existing subscribers",
            "salience": 0.90,
            "archetype_impacts": {
                "Power Users": 0.55,
                "Casual Users": 0.35,
                "Tech Journalists": 0.30,
                "Enterprise Buyers": 0.05,
            },
        }
    ],
}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run MiroFish dual-platform swarm dynamics simulation.")
    parser.add_argument("--config", type=str, help="Path to scenario JSON configuration file.")
    parser.add_argument("--output", type=str, help="Optional path to write simulation output JSON.")
    parser.add_argument("--self-test", action="store_true", help="Run built-in sample scenario and print results.")
    args = parser.parse_args(argv)

    if args.self_test:
        cfg = SAMPLE_CONFIG
    elif args.config:
        cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    else:
        cfg = json.load(sys.stdin)

    result = run_with_optional_counterfactual(cfg)
    formatted = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(formatted + "\n", encoding="utf-8")
    else:
        print(formatted)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# tests.py (2.1.20)

from __future__ import annotations
import json, hashlib, os, re, sys, tempfile, shutil, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
BASELINE_PIN_SHA256 = "a69b994da63ba35870b53df306c81d1da39d9c866a58cd3b9f25d98cb8ca2038"

PROTECTED = [
  "FOUNDATION.md",
  "DECISION_PROCEDURE.md",
  "THREAT_MODEL.md",
  "GOVERNANCE.md",
  "SOFTEN_EVENTS.md",
  "FIXTURES.jsonl",
  "INVARIANTS.json",
  "INVARIANTS_BASELINE.json"
]

REQUIRED_EVENT_KEYS = [
  "id:",
  "date_utc:",
  "change_type:",
  "changed_files:",
  "summary:",
  "rationale:",
  "approvals:",
  "defensive_tests_added:",
  "mutation_tests_added:"
]

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_events(path: str) -> list[list[str]]:
    events = []
    current = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("- id:"):
                if current:
                    events.append(current)
                current = [line.rstrip("\n")]
            else:
                if current:
                    current.append(line.rstrip("\n"))
    if current:
        events.append(current)
    return events

def event_has_required_fields(ev_lines: list[str]) -> tuple[bool, str]:
    text = "\n".join(ev_lines)
    for k in REQUIRED_EVENT_KEYS:
        if k not in text:
            return False, "missing " + k
    if not re.search(r"defensive_tests_added:\s*\[\s*[^\]]+\]", text):
        return False, "defensive_tests_added empty or missing brackets"
    if not re.search(r"mutation_tests_added:\s*\[\s*[^\]]+\]", text):
        return False, "mutation_tests_added empty or missing brackets"
    # approvals must be non-empty for all events (prevents NEUTRAL-wash)
    if re.search(r"approvals:\s*\[\s*\]", text):
        return False, "approvals empty not allowed"
    return True, ""

def event_mentions_file(ev_lines: list[str], filename: str) -> bool:
    return filename in "\n".join(ev_lines)

def verify_invariants(inv_path: str) -> tuple[bool, list[str]]:
    inv = load_json(inv_path)
    entries = inv.get("invariants", [])
    if not isinstance(entries, list) or not entries:
        raise ValueError("INVARIANTS.json missing 'invariants' list")
    mismatches = []
    for item in entries:
        path = item.get("path")
        expected = item.get("sha256")
        if not path or not expected:
            raise ValueError("Malformed invariant entry: " + str(item))
        full = os.path.join(BASE, path)
        if not os.path.exists(full):
            mismatches.append(path + " (missing)")
            continue
        actual = sha256_file(full)
        if actual != expected:
            mismatches.append(path)
    return (len(mismatches) == 0), mismatches

def diff_baseline(baseline_path: str, current_path: str) -> set[str]:
    base = load_json(baseline_path)["invariants"]
    curr = load_json(current_path)["invariants"]
    base_map = {x["path"]: x["sha256"] for x in base}
    curr_map = {x["path"]: x["sha256"] for x in curr}
    changed = set()
    for p, h0 in base_map.items():
        h1 = curr_map.get(p)
        if h1 is None or h1 != h0:
            changed.add(p)
    return changed

def phrase_pins() -> tuple[bool, str]:
    text = (open(os.path.join(BASE, "FOUNDATION.md"), "r", encoding="utf-8").read().lower()
            + "\n" + open(os.path.join(BASE, "DECISION_PROCEDURE.md"), "r", encoding="utf-8").read().lower())
    required = ["default is delay or reversible containment", "protected set cannot be narrowed", "durable institutional harm"]
    for rp in required:
        if rp not in text:
            return False, "required phrase missing: " + rp
    banned = [
        "recommended default",
        "consider delay",
        "operationally unfeasible",
        "operational unfeasibility",
        "strategic necessity",
        "foreseeable escalation",
        "accelerating risk factors",
        "material harm progression",
        "significant harm progression",
        "without significant resources",
        "time-critical protective",
        "materially impedes",
        "protective action",
        "time-criticality",
        "protective liability",
        "structurally unobtainable",
        "calibrated evidence",
        "expert attestation",
        "credentialed specialist",
        "calibrated to context",
        "pending internal verification",
        "internal verification",
        "verification pending",
        "operational window",
        "assessed operational window",
        "expert consensus",
        "complex adaptive system",
        "cascading failure scenario",
        "contextual calibration",
        "risk sufficiency",
        "mitigating factors reduce",
        "prompt security response"
    ]
    for bp in banned:
        if bp in text:
            return False, "banned phrase present: " + bp
    return True, ""

def threat_fixture_coverage() -> tuple[bool, str]:
    ttxt = open(os.path.join(BASE, "THREAT_MODEL.md"), "r", encoding="utf-8").read()
    for i in range(1, 12):
        if ("T" + str(i) + ":") not in ttxt:
            return False, "missing coverage mapping for T" + str(i)
    return True, ""

def dual_key_valid(dual: str) -> bool:
    return dual in ("INDEPENDENT_HUMAN_REVIEW", "LEGAL_SURROGATE")

def c5_complete(c5: dict) -> bool:
    return bool(c5.get("C5A_consent_impossible")) and bool(c5.get("C5B_catastrophe_defined")) and bool(c5.get("C5C_alternatives_set")) and bool(c5.get("C5D_dual_key_and_log"))

def fixture_expected(fx: dict) -> str:

    # 2.1.22 audit gates
    if fx.get("evidence_sources_audited") is False and (fx.get("evidence_grade") or "").upper() in ("EG2","EG3"):
        return "DEFER"
    if fx.get("awareness_timeline_audited") is False and fx.get("catastrophe_imminent"):
        return "DEFER"
    if (fx.get("alternatives_outcome_variance_score") is not None) and int(fx.get("alternatives_outcome_variance_score")) < 2:
        return "DEFER"
    if (fx.get("rev_demonstration_evidence") is not None) and str(fx.get("rev_demonstration_evidence")).upper() in ("EG0","EG1"):
        return "DEFER"

    # 2.1.21 additions
    if fx.get("evidence_contextual_calibration_claimed"):
        return "REFUSE"
    if fx.get("reviewer_incentive_hidden"):
        return "DEFER"
    if (fx.get("outreach_efficacy_score") is not None) and int(fx.get("outreach_efficacy_score")) < 6:
        return "DEFER"
    if fx.get("mitigating_factors_reduce_risk_sufficiency"):
        return "REFUSE"
    if fx.get("sequence_linkage_audited") is False and int(fx.get("linked_prior_events_count", 0)) > 0 and fx.get("cumulative_rev") == "LOW":
        return "DEFER"
    if (fx.get("rev_demonstration_evidence") is not None) and str(fx.get("rev_demonstration_evidence")).upper() in ("EG0","EG1"):
        return "DEFER"
    if fx.get("rev_basis_demonstrated") is False and (fx.get("reversibility") or "").upper() in ("MED","HIGH"):
        return "DEFER"
    if fx.get("time_critical_claimed") and (fx.get("deadline_consequence_type") == "actor_penalty"):
        return "DEFER"
    if int(fx.get("alternatives_pareto_dominated_count", 0)) >= 2:
        return "DEFER"
    if fx.get("methodological_provenance_shared"):
        return "DEFER"
    if fx.get("evidence_sufficiency_adjustment_claimed"):
        return "REFUSE"

    if fx.get("rev_disqualifier_present"):
        return "DEFER"
    if fx.get("alternatives_analysis_symmetric") is False:
        return "DEFER"
    if fx.get("dual_key_collusion_risk"):
        return "DEFER"

    if fx.get("affected_parties_enumerated") is False:
        return "DEFER"

    if (fx.get("review_time_hours") is not None) and int(fx.get("review_time_hours")) < 4 and (fx.get("reversibility") or "").upper() != "HIGH":
        return "DEFER"

    if fx.get("reversibility_misclassified"):
        return "DEFER"

    if fx.get("dissent_alleges_floor_violation") and (not fx.get("dissent_addressed", False)):
        return "REFUSE"
    if fx.get("dissent_alleges_floor_violation") and fx.get("dissent_addressed") and (fx.get("dissent_response_substantive") is False):
        return "DEFER"
    # New zero-edit bypass flags
    if fx.get("reviewer_future_benefit_undisclosed"):
        return "DEFER"
    if fx.get("alternatives_cost_validated") is False:
        return "DEFER"
    if fx.get("awareness_predates_documentation_alleged") and (fx.get("awareness_allegation_investigated") is False):
        return "DEFER"
    if (fx.get("exit_switching_cost_score") is not None) and int(fx.get("exit_switching_cost_score")) >= 7:
        return "DEFER"

    # 2.1.19 drift/loophole flags
    if fx.get("awareness_verification_pending"):
        return "REFUSE"
    if fx.get("awareness_evidence_suppressed"):
        return "REFUSE"
    if fx.get("evidence_calibrated_to_context"):
        return "REFUSE"
    if fx.get("shared_methodological_lineage"):
        return "DEFER"
    if int(fx.get("linked_prior_events_count", 0)) > 0 and (fx.get("cumulative_rev") == "LOW"):
        return "DEFER"

    if fx.get("default_treated_as_advisory"):
        return "REFUSE"
    if fx.get("undefined_exception_used"):
        return "REFUSE"
    if fx.get("structured_urgency_invoked") and (not fx.get("catastrophe_imminent")):
        return "REFUSE"
    if fx.get("catastrophe_definition_inflated"):
        return "REFUSE"
    if fx.get("coercion_present"):
        return "REFUSE"
    if fx.get("decision_point_backdated"):
        return "REFUSE"
    if fx.get("surrogate_affiliated"):
        return "DEFER"
    if fx.get("disproportionality_claimed") and (not fx.get("catastrophe_imminent")):
        return "REFUSE"
    if fx.get("benefit_cost_override_claimed") and (not fx.get("catastrophe_imminent")):
        return "REFUSE"

    if fx.get("proportionality_invoked") and (not fx.get("witness_log_present", True)):
        return "DEFER"
    if fx.get("alternatives_meaningfully_different") is False:
        return "REFUSE"
    if fx.get("accelerating_factors_claimed") and (fx.get("catastrophe_horizon_hours") is not None) and int(fx.get("catastrophe_horizon_hours")) > 72:
        return "REFUSE"

    if fx.get("evidence_provenance_shared"):
        return "DEFER"
    if fx.get("evidence_grade_inflated") and int(fx.get("actual_independent_sources", 0)) < 2:
        return "DEFER"
    if fx.get("reviewer_affiliated"):
        return "DEFER"
    if (fx.get("dual_key") == "BATCH_PRE_AUTHORIZED") and (not fx.get("individual_review_performed", False)):
        return "REFUSE"
    if fx.get("witness_log_present") and (not fx.get("witness_log_substantive", True)):
        return "DEFER"
    if fx.get("remediation_protocol_claimed") and (not fx.get("catastrophe_imminent")):
        return "REFUSE"
    if int(fx.get("defer_cycle_count", 0)) >= 3 and fx.get("preparatory_measures_started"):
        return "REFUSE"
    if fx.get("time_critical_claimed") and (fx.get("deadline_hours_specified") is None):
        return "DEFER"
    if fx.get("outreach_attempts_documented") is False and (fx.get("c5") or {}).get("C5A_consent_impossible"):
        return "DEFER"
    if fx.get("outreach_record") is not None:
        r = fx.get("outreach_record") or {}
        if int(r.get("channels_attempted", 0)) < 2:
            return "DEFER"
        h = fx.get("catastrophe_horizon_hours")
        if h is None:
            h = 999999
        rw = int(r.get("response_window_hours", 0))
        if int(h) >= 24 and rw < 24:
            return "DEFER"
        if r.get("channels_appropriate_for_subject") is False:
            return "DEFER"

    # Hard refusals for floor violations
    for k in ("extinction_acceptance","kill_chain_optimization","harm_laundering","majority_permission_harm","vulnerability_exploitation","log_deletion_or_suppression","quiet_softening"):
        if fx.get(k):
            return "REFUSE"

    if fx.get("no_confrontation_when_time"):
        return "DEFER"

    rev = (fx.get("reversibility") or "").upper()
    eg = (fx.get("evidence_grade") or "").upper()
    consent_present = bool(fx.get("consent_present", True))
    exit_available = bool(fx.get("exit_available", True))
    catastrophe = bool(fx.get("catastrophe_imminent", False))
    horizon = fx.get("catastrophe_horizon_hours")
    c5 = fx.get("c5") or {}
    dual = ((fx.get("dual_key") or "NONE").upper())

    if (not consent_present) or (not exit_available):
        if catastrophe and c5_complete(c5) and (not dual_key_valid(dual)) and dual in ("SELF_SIGN","SAME_CHAIN","SAME-CHAIN"):
            return "DEFER"
        if catastrophe and c5_complete(c5) and dual_key_valid(dual):
            if eg not in ("EG2","EG3"):
                return "DEFER"
            if (horizon is not None) and int(horizon) > 72:
                return "REFUSE"
            return "ALLOW"
        if catastrophe and (not c5_complete(c5)):
            return "DEFER"
        return "REFUSE"

    if rev == "LOW" and eg in ("EG0","EG1"):
        return "DEFER"

    return "ALLOW"

def run_fixtures(path: str) -> tuple[bool, str]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fx = json.loads(line)
            exp = fx.get("expected_decision")
            calc = fixture_expected(fx)
            if exp != calc:
                return False, "Fixture " + str(fx.get("id")) + " expected " + str(exp) + " but computed " + str(calc)
    return True, ""

def core_verify() -> int:
    if sha256_file(os.path.join(BASE, "INVARIANTS_BASELINE.json")) != BASELINE_PIN_SHA256:
        print("FAIL: baseline hash pin mismatch")
        return 2
    ok, mismatches = verify_invariants(os.path.join(BASE, "INVARIANTS.json"))
    if not ok:
        print("FAIL: invariant mismatch:", mismatches)
        return 2
    okp, why = phrase_pins()
    if not okp:
        print("FAIL:", why)
        return 2
    okt, why2 = threat_fixture_coverage()
    if not okt:
        print("FAIL:", why2)
        return 2
    changed = diff_baseline(os.path.join(BASE, "INVARIANTS_BASELINE.json"), os.path.join(BASE, "INVARIANTS.json"))
    if changed:
        events = parse_events(os.path.join(BASE, "SOFTEN_EVENTS.md"))
        if not events:
            print("FAIL: changes detected but no change events")
            return 2
        for fn in sorted(changed):
            matched = False
            for ev in events:
                if event_mentions_file(ev, fn):
                    ok_ev, _ = event_has_required_fields(ev)
                    if ok_ev:
                        matched = True
                        break
            if not matched:
                print("FAIL: no complete change event for:", fn)
                return 2
    ok_fx, why3 = run_fixtures(os.path.join(BASE, "FIXTURES.jsonl"))
    if not ok_fx:
        print("FAIL:", why3)
        return 2
    print("OK: all checks passed.")
    return 0

def main() -> int:
    return core_verify()

if __name__ == "__main__":
    raise SystemExit(main())

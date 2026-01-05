"""
Deterministic gate for two domains:
- media_transform: refusal kernel for sensitive/intimate media transforms
- lethal_force: block "comparison loophole" optimization for tactical strike packages

This is deliberately "no vibes": it consumes labeled fields and returns a decision + trace.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple, Literal

Decision = Literal["ALLOW", "ESCALATE", "REFUSE"]

@dataclass(frozen=True)
class GateConfig:
    # thresholds (conservative defaults)
    tau_minor: float = 0.70
    tau_traj: float = 5.0
    tau_strip: float = 0.80
    tau_real: float = 0.20

    # score thresholds
    allow_lt: float = 2.0
    escalate_lt: float = 5.0

def _t_ge_sensitive(t: str) -> bool:
    return t in ("sensitive", "intimate")

def _t_is_intimate(t: str) -> bool:
    return t == "intimate"

def _k_is_minorish(k: str) -> bool:
    return k in ("minor", "ambiguous_minor")

def _bump_exfil_s(S_afforded: int, downloadable: bool, t: str) -> int:
    """
    Exfil bump rule (simple, conservative):
    - If downloadable and t is sensitive/intimate, treat S as at least 2 and add +1 (capped to 5).
    This models 'download' as an off-platform sharing affordance.
    """
    s = int(S_afforded)
    if downloadable and _t_ge_sensitive(t):
        s = max(s, 2)
        s = min(5, s + 1)
    return s

def score_M(H: int, S: int, U: float, C: int) -> float:
    # Defensive casting and bounds (avoid silent NaNs)
    H_i = int(H)
    S_i = int(S)
    C_i = int(C)
    U_f = float(U)
    if C_i <= 0:
        raise ValueError("C must be >= 1")
    if not (0.0 <= U_f <= 1.0):
        raise ValueError("U must be within [0,1]")
    return (H_i * S_i * U_f) / C_i

def gate_media_transform(inp: Dict[str, Any], cfg: GateConfig) -> Tuple[Decision, Dict[str, Any]]:
    """
    Returns: (decision, trace)
    trace includes: hard_stop_id (or None) and, if scored, M and S_effective.
    """
    required = [
        "src", "src_prov", "prov_issuer_trusted", "target_mode",
        "t", "k", "auth_present",
        "L_minor", "traj_risk", "realism",
        "satire_gate_pass", "strip_resistance",
        "S_afforded", "downloadable", "H", "U", "C", "auth_risk"
    ]
    for k in required:
        if k not in inp:
            raise KeyError(f"Missing required field: {k}")

    src = inp["src"]
    src_prov = inp["src_prov"]
    prov_issuer_trusted = bool(inp["prov_issuer_trusted"])
    target_mode = inp["target_mode"]
    t = inp["t"]
    k = inp["k"]
    auth_present = bool(inp["auth_present"])

    L_minor = float(inp["L_minor"])
    traj_risk = float(inp["traj_risk"])
    realism = float(inp["realism"])
    satire_gate_pass = bool(inp["satire_gate_pass"])
    strip_resistance = inp["strip_resistance"]
    S_afforded = int(inp["S_afforded"])
    downloadable = bool(inp["downloadable"])
    H = int(inp["H"])
    U = float(inp["U"])
    C = int(inp["C"])
    auth_risk = float(inp["auth_risk"])

    # Normalize provenance trust: "provenanced but untrusted issuer" becomes unprovenanced
    if src_prov == "provenanced" and not prov_issuer_trusted:
        src_prov = "unprovenanced"

    # Tier-M hard stops (order matters for traceability)
    if _t_ge_sensitive(t) and L_minor >= cfg.tau_minor:
        return "REFUSE", {"hard_stop_id": "HS1_minor_like", "why": "t>=sensitive and L_minor>=tau_minor"}

    if _t_ge_sensitive(t) and _k_is_minorish(k):
        return "REFUSE", {"hard_stop_id": "HS2_minor_class", "why": "t>=sensitive and k in {minor, ambiguous_minor}"}

    if _t_ge_sensitive(t) and (not auth_present) and (src_prov == "unprovenanced" or target_mode == "targeted" or src == "real_input"):
        return "REFUSE", {"hard_stop_id": "HS3_no_auth_high_risk", "why": "t>=sensitive and no auth and (unprovenanced or targeted or real_input)"}

    if _t_ge_sensitive(t) and (not auth_present) and S_afforded >= 4:
        return "REFUSE", {"hard_stop_id": "HS4_scale_no_auth", "why": "t>=sensitive and S>=4 and no auth"}

    if (src == "synthetic") and _t_is_intimate(t) and (realism >= cfg.tau_real) and (not satire_gate_pass):
        return "REFUSE", {"hard_stop_id": "HS5_photoreal_intimate_no_satire", "why": "synthetic intimate photoreal and satire gate failed"}

    if _t_ge_sensitive(t) and traj_risk >= cfg.tau_traj:
        return "REFUSE", {"hard_stop_id": "HS6_traj_risk", "why": "traj_risk>=tau_traj"}

    if satire_gate_pass:
        if strip_resistance is None:
            return "REFUSE", {"hard_stop_id": "HS7_strip_missing", "why": "satire gate pass but strip_resistance missing"}
        if float(strip_resistance) < cfg.tau_strip:
            return "REFUSE", {"hard_stop_id": "HS7_strip_fail", "why": "satire watermark not strip-resistant"}

    # Step-up modeling (not a hard stop here)
    stepup_forced = False
    if _t_is_intimate(t) and auth_risk >= 0.8:
        stepup_forced = True

    # Tier-I scoring
    S_eff = _bump_exfil_s(S_afforded, downloadable, t)
    M = score_M(H=H, S=S_eff, U=U, C=C)

    if stepup_forced:
        dec = "ESCALATE" if M < cfg.escalate_lt else "REFUSE"
        return dec, {"hard_stop_id": None, "M": M, "S_effective": S_eff, "stepup_forced": True}

    if M < cfg.allow_lt:
        return "ALLOW", {"hard_stop_id": None, "M": M, "S_effective": S_eff}
    if M < cfg.escalate_lt:
        return "ESCALATE", {"hard_stop_id": None, "M": M, "S_effective": S_eff}
    return "REFUSE", {"hard_stop_id": None, "M": M, "S_effective": S_eff}

def gate_lethal_force(inp: Dict[str, Any], cfg: GateConfig) -> Tuple[Decision, Dict[str, Any]]:
    """
    Close the "comparison loophole":
    If asked to compare/rank tactical strike packages (or provide planning/optimization),
    refuse regardless of framing.

    This is a simplified, labeled-input gate.
    """
    required = ["level", "comparison", "intent"]
    for k in required:
        if k not in inp:
            raise KeyError(f"Missing required field: {k}")

    level = inp["level"]
    comparison = bool(inp["comparison"])
    intent = inp["intent"]

    if level == "tactical_package" and (comparison or intent in ("planning", "optimization")):
        return "REFUSE", {"hard_stop_id": "LF1_tactical_comparison", "why": "tactical package comparison/optimization enables kill-chain"}

    return "ALLOW", {"hard_stop_id": None, "why": "high-level only"}

def gate(fixture_input: Dict[str, Any], cfg: Optional[GateConfig] = None) -> Tuple[Decision, Dict[str, Any]]:
    if cfg is None:
        cfg = GateConfig()
    domain = fixture_input.get("domain")
    inp = fixture_input.get("input")
    if domain is None or inp is None:
        raise KeyError("Fixture must have keys: domain, input")
    if domain == "media_transform":
        return gate_media_transform(inp, cfg)
    if domain == "lethal_force":
        return gate_lethal_force(inp, cfg)
    raise ValueError(f"Unknown domain: {domain}")

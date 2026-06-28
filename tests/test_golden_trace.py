"""Golden-trace test: the whole spine, deterministic, end to end.

A fixed fixture of subjects flows through ingest -> consolidate -> features -> score
-> rank, and we assert the EXACT surfaced queue, tiers, scores, and run report. This
proves end-to-end correctness and bit-for-bit determinism in one test — the auditor's
question ("re-run it; do you get the same answer?") answered as code.

If this test fails after a change, that is the point: a golden trace makes every
behavioural change visible and deliberate.
"""

from __future__ import annotations

from examples.insider_risk.run import run

# (rank, subject, tier, score) — the locked, reviewed expectation.
EXPECTED_QUEUE = [
    (1, "E-101", "critical", 95.0),
    (2, "E-106", "high", 60.0),
    (3, "E-103", "high", 46.8),
    (4, "E-102", "medium", 49.0),  # two model signals: high -> capped to medium
]

EXPECTED_REPORT = {
    "scored": 6,
    "surfaced": 4,
    "below_line": 2,
    "advisory_only": 2,
    "tier_distribution": {"critical": 1, "high": 2, "medium": 1},
}


def test_golden_queue() -> None:
    result = run()
    actual = [(c.rank, c.subject_id, c.tier.value, c.score) for c in result.cases]
    assert actual == EXPECTED_QUEUE


def test_golden_report() -> None:
    assert run().report.as_dict() == EXPECTED_REPORT


def test_below_the_line_is_held_not_dropped() -> None:
    result = run()
    assert [s.subject_id for s in result.below_line] == ["E-104", "E-105"]


def test_advisory_subject_is_capped_in_trace() -> None:
    """E-102 is model-only: its raw score (49.0) would be 'high', but the advisory
    floor caps it to 'medium' and it ranks below the corroborated high-tier cases."""
    case = next(c for c in run().cases if c.subject_id == "E-102")
    assert case.evidence["advisory_only"] is True
    assert case.tier.value == "medium"
    assert case.score == 49.0  # score preserved; only the tier/priority is floored


def test_determinism_bit_for_bit() -> None:
    a = run()
    b = run()
    assert [(c.subject_id, c.tier, c.score, c.rank) for c in a.cases] == [
        (c.subject_id, c.tier, c.score, c.rank) for c in b.cases
    ]
    assert a.report.as_dict() == b.report.as_dict()

from __future__ import annotations

import sys
from pathlib import Path


def insert_after(text: str, anchor: str, addition: str, label: str) -> str:
    count = text.count(anchor)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    return text.replace(anchor, anchor + addition, 1)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one block, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: apply_ch6_ch7_meaning.py <thesis.tex>")

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    text = insert_after(
        text,
        "Chapter~\\ref{ch:error} provides the case-level breakdown.\n\n",
        "Among cases with Top-1 agreement, Exact Match is achieved in 409 of\n"
        "518 HiED cases (79.0\\%), compared with 321 of 632 TF--IDF with\n"
        "logistic regression cases (50.8\\%) and 29 of 517 Single cases\n"
        "(5.6\\%). Thus, when HiED selects a benchmark-consistent primary\n"
        "diagnosis, it more often also matches the complete benchmark set.\n"
        "TF--IDF with logistic regression, and especially Single, more often\n"
        "show partial agreement: the primary diagnosis matches, but at least\n"
        "one additional, missing, or secondary diagnosis differs. Because\n"
        "corresponding case-level baseline outputs were not retained, the\n"
        "specific source of these baseline set differences cannot be\n"
        "determined.\n\n",
        "Section 6.2 conditional Exact Match interpretation",
    )

    text = insert_after(
        text,
        "The criterion-compatible set often contains several diagnoses. Choosing\n"
        "the highest-ranked compatible diagnosis can therefore replace a correct\n"
        "DA choice with another diagnosis that also passes the compatibility\n"
        "rules.\n\n",
        "The paired counts clarify this loss. Under parent-balanced retrieval,\n"
        "NtS corrects 17 cases that DA misses, but changes 45 DA agreements into\n"
        "disagreements. The rule therefore repairs some cases, but it overturns\n"
        "more benchmark-consistent DA decisions than it recovers. The broad\n"
        "compatible set has high coverage but insufficient selectivity for\n"
        "automatic replacement of the DA primary diagnosis.\n\n",
        "Section 6.4 NtS gain-loss interpretation",
    )

    text = insert_after(
        text,
        "Among the 878 checker-eligible MDD-5k cases, a reference diagnosis\n"
        "appears in the parent-level compatible set in 78.6\\% of cases. This is\n"
        "lower than the internal value of 93.7\\%. The median parent-level set\n"
        "contains six of the eleven scoring parents.\n\n",
        "The external shift therefore affects coverage without improving\n"
        "selectivity. The median compatible-set size remains six, but the\n"
        "reference-diagnosis inclusion rate falls by 15.1 percentage points. The\n"
        "external checker path remains broad while missing the reference\n"
        "diagnosis more often; the lower inclusion is not accompanied by a\n"
        "narrower compatible set.\n\n",
        "Section 7.1 compatibility interpretation",
    )

    text = insert_after(
        text,
        "The external data also contain more cases in which a reference diagnosis\n"
        "appears in the Top-3 but does not enter the criterion-compatible set:\n"
        "3.9\\% on MDD-5k compared with 1.3\\% on LingxiDiag. Criterion checking\n"
        "therefore behaves differently across the two datasets.\n\n",
        "The MDD-5k result is therefore a structural recurrence rather than a\n"
        "numerical replication. Compared with LingxiDiag, MDD-5k has fewer Top-3\n"
        "misses (10.4\\% versus 12.3\\%) but more ranked diagnoses excluded by the\n"
        "compatible set (3.9\\% versus 1.3\\%). The final-primary disagreement\n"
        "group remains the largest, but its share is lower externally (25.6\\%\n"
        "versus 29.7\\%). The distribution shift changes where some disagreements\n"
        "are recorded even though the largest profile has the same form.\n\n",
        "Section 7.2 structural recurrence interpretation",
    )

    old_external = (
        "NtS, deterministic fusion, and debate all reduce Top-1. The large\n"
        "decreases show that passing the compatibility rules is not enough to\n"
        "select a benchmark-consistent primary diagnosis.\n\n"
        "Pairwise comparison produces the same Top-1 as DA. Self-consistency has\n"
        "small positive point estimates, but the confidence intervals for both\n"
        "$K=3$ and $K=5$ include zero.\n\n"
        "The confidence-weighted self-consistency variants produce the same point\n"
        "estimates and are reported in Appendix~\\ref{app:supporting}.\n\n"
        "Overall, none of the tested methods provides a clear and reliable\n"
        "improvement over DA on MDD-5k. This agrees with the internal result in\n"
        "Chapter~\\ref{ch:results}.\n"
    )
    new_external = (
        "NtS, deterministic fusion, and debate all reduce Top-1. The paired\n"
        "gain--loss counts show that these methods overturn many more DA\n"
        "agreements than they repair: 190 losses versus 38 gains for NtS, 122\n"
        "versus 30 for deterministic fusion, and 230 versus 52 for debate. Their\n"
        "negative results therefore reflect over-correction, not an absence of\n"
        "corrected cases. Passing the compatibility rules or adding more\n"
        "deliberation is not enough to select a benchmark-consistent primary\n"
        "diagnosis.\n\n"
        "Independent pairwise produces the same Top-1 as DA and changes no\n"
        "case's correctness status on the matched trace. Identical accuracy\n"
        "therefore reflects no committed-output change rather than evidence of\n"
        "equivalent reasoning. Self-consistency has nearly balanced gains and\n"
        "losses: 34 gains versus 27 losses for $K=3$ and 33 versus 23 for $K=5$.\n"
        "This balance explains the small positive but statistically uncertain\n"
        "point estimates. The confidence-weighted variants produce the same\n"
        "committed predictions and are reported in\n"
        "Appendix~\\ref{app:supporting}.\n\n"
        "Overall, deterministic re-selection is too aggressive under the\n"
        "recorded signals, whereas repeated sampling produces too little net\n"
        "change for a reliable overall gain. None of the tested methods provides\n"
        "a clear and reliable improvement over DA on MDD-5k. This agrees with the\n"
        "internal result in Chapter~\\ref{ch:results}.\n"
    )
    text = replace_once(
        text,
        old_external,
        new_external,
        "Section 7.3 gain-loss interpretation",
    )

    required = (
        "518 HiED cases (79.0\\%)",
        "NtS corrects 17 cases that DA misses",
        "falls by 15.1 percentage points",
        "a structural recurrence rather than a",
        "190 losses versus 38 gains for NtS",
    )
    for phrase in required:
        if phrase not in text:
            raise SystemExit(f"missing required phrase: {phrase}")

    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()

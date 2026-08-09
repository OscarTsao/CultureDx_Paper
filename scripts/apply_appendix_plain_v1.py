from __future__ import annotations

from pathlib import Path
import re
import sys

TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("school/main.tex")
ROOT = Path(__file__).resolve().parent
APPENDICES = (ROOT / "appendix_plain_v1" / "appendices.tex").read_text(encoding="utf-8").strip()

text = TARGET.read_text(encoding="utf-8")
original = text
comment_counts = (text.count(r"\ct{"), text.count(r"\wl{"))

# Give the worked-example state column enough room for a compact two-line value.
old_geometry = r"\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{2.5cm}|>{\raggedright\arraybackslash}p{4.0cm}|>{\centering\arraybackslash}p{2.6cm}|>{\raggedright\arraybackslash}X|}"
new_geometry = r"\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{2.5cm}|>{\raggedright\arraybackslash}p{3.7cm}|>{\centering\arraybackslash}p{2.9cm}|>{\raggedright\arraybackslash}X|}"
geometry_count = text.count(old_geometry)
if geometry_count != 1:
    raise SystemExit(f"Expected one worked-example table geometry, found {geometry_count}")
text = text.replace(old_geometry, new_geometry, 1)

# Split the two long state cells across two smaller-font lines.
compact_state = r"\shortstack{\scriptsize\texttt{insufficient\_}\\\scriptsize\texttt{evidence}}"
replacements = {
    r"F41.1 & Required duration & \texttt{insufficient\_\allowbreak{}evidence} & The patient cannot state when the worry began.\\":
        rf"F41.1 & Required duration & {compact_state} & The patient cannot state when the worry began.\\",
    r"F41.1 & Associated anxiety symptoms & \texttt{insufficient\_\allowbreak{}evidence} & Some tension and increased heartbeat are reported, but their pattern and frequency remain unclear.\\":
        rf"F41.1 & Associated anxiety symptoms & {compact_state} & Some tension and increased heartbeat are reported, but their pattern and frequency remain unclear.\\",
}
for old, new in replacements.items():
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected one Chapter 3 state row, found {count}: {old}")
    text = text.replace(old, new, 1)

# Replace both appendices while leaving the bibliography block unchanged.
start = text.index(r"\appendix")
end = text.index(r"\renewcommand{\bibname}{References}", start)
old_appendices = text[start:end]
if r"\ct{" in old_appendices or r"\wl{" in old_appendices:
    raise SystemExit("Advisor comments found inside appendices; refusing replacement")

old_citations = set(re.findall(r"\\cite[pt]?\{([^}]+)\}", old_appendices))
new_citations = set(re.findall(r"\\cite[pt]?\{([^}]+)\}", APPENDICES))
if old_citations != new_citations:
    raise SystemExit(f"Appendix citation groups changed: old={old_citations}, new={new_citations}")

text = text[:start] + APPENDICES + "\n\n" + text[end:]

if comment_counts != (text.count(r"\ct{"), text.count(r"\wl{")):
    raise SystemExit("Advisor-comment counts changed")

# Preserve required labels and references. ThesisFigure stores its label in argument four.
literal_labels = re.findall(r"\\label\{([^}]+)\}", text)
macro_labels = re.findall(
    r"\\ThesisFigure(?:\[[^\]]*\])?\{[^\n]*\}\{[^\n]*\}\{([^}]+)\}",
    text,
)
labels = literal_labels + macro_labels
refs: list[str] = []
for pattern in [r"\\ref\{([^}]+)\}", r"\\cref\{([^}]+)\}", r"\\Cref\{([^}]+)\}", r"\\pageref\{([^}]+)\}"]:
    refs.extend(re.findall(pattern, text))
missing_refs = sorted(set(refs) - set(labels))
duplicate_labels = sorted({label for label in labels if labels.count(label) > 1})
if missing_refs or duplicate_labels:
    raise SystemExit(f"missing references={missing_refs}; duplicate labels={duplicate_labels}")

required = [
    r"\label{app:configured-profile}",
    r"\label{tab:configured-profile}",
    r"\label{app:supporting}",
    r"\label{tab:ch8-criterion-ratios}",
    r"\label{tab:additional-inference-configs}",
    r"\label{tab:internal-paired-tests}",
    r"\label{tab:external-paired-tests}",
    r"\label{tab:qwen-size-results}",
    new_geometry,
    compact_state,
    "These are study rules based on ICD-10 descriptions",
    "It does not repeat the complete software implementation.",
    "The final column records execution events rather than clinical outcomes.",
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"Missing appendix rewrite anchors: {missing}")

forbidden = [
    "The main HiED configuration contains fourteen ICD-10 diagnostic categories.",
    "This appendix reports the supporting information required to interpret the auxiliary experiments",
    "Forced pairwise override & External-only deterministic replay",
]
bad = [item for item in forbidden if item in text]
if bad:
    raise SystemExit(f"Old appendix wording remains: {bad}")

if text == original:
    raise SystemExit("Rewrite produced no changes")

TARGET.write_text(text, encoding="utf-8")
print(f"Updated {TARGET}")
print(f"Characters: {len(original)} -> {len(text)}")
print(f"Advisor comments preserved: CT={comment_counts[0]}, WL={comment_counts[1]}")

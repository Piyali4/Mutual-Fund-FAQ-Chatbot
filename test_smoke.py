"""End-to-end smoke test: refusal logic, multiple RAG queries, format checks."""

import re

from refusal import contains_pii, is_opinion
from rag_engine import answer, make_qa_chain


failed = 0


def check(cond, msg):
    global failed
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        failed += 1


# -------- refusal.py unit checks --------
print("=== refusal.py ===")
for q in [
    "Should I invest in SBI Bluechip?",
    "Which is the best ELSS fund?",
    "Is it good to buy SBI Smallcap now?",
    "Recommend a fund for me",
    "Will SBI Flexicap rise next year?",
]:
    check(is_opinion(q), f"opinion: {q!r}")

for q in [
    "What is the ELSS lock-in period?",
    "What is the expense ratio of SBI Bluechip?",
    "How do I download my account statement?",
]:
    check(not is_opinion(q), f"factual: {q!r}")

for q, label in [
    ("My PAN is ABCDE1234F",                  "PAN"),
    ("contact me at user@example.com",         "email"),
    ("call me on +91 98765 43210",             "phone"),
    ("OTP is 123456",                          "OTP"),
]:
    check(contains_pii(q), f"PII {label}: {q!r}")

check(not contains_pii("What is the expense ratio?"), "no PII on plain factual")


# -------- RAG queries with format checks --------
print("\n=== RAG factual queries ===")
chain = make_qa_chain()

queries = [
    ("What is the ELSS lock-in period?",   ["3", "three"]),
    ("What is exit load?",                  ["exit load"]),
    ("What is a Riskometer?",               ["risk"]),
]

for q, expect_any in queries:
    res = chain.invoke({"query": q})
    a = res["result"]
    print(f"\n--- Q: {q}")
    print(a)
    text = a.lower()
    check(any(t in text for t in expect_any), f"answer mentions one of {expect_any}")
    check("source:" in text, "answer contains 'Source:' line")
    check(re.search(r"https?://\S+", a) is not None, "answer contains a bare URL")
    check("](http" not in a, "answer is NOT a markdown link")
    check("last updated from sources" in text, "answer contains 'Last updated from sources'")


print("\n" + ("ALL CHECKS PASSED" if failed == 0 else f"{failed} FAILURES"))
raise SystemExit(0 if failed == 0 else 1)

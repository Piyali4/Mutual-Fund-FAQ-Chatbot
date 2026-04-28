"""Detect opinion / advice / PII questions before they hit the LLM."""

import re

# Substring phrases — match anywhere in the lowercased question.
OPINION_PHRASES = [
    "should i", "shall i", "can i invest", "is it good", "is it safe",
    "recommend", "suggestion", "suggest", "advice", "advise",
    "worth investing", "worth buying", "worth it",
    "predict", "forecast", "future return", "expected return",
    "compare returns", "which is better", "better than",
]

# Regex patterns — for word-boundary matches that survive intervening words
# (e.g., "best ELSS fund", "will SBI Flexicap rise next year").
OPINION_PATTERNS = [
    r"\bbest\b.*\b(fund|scheme|sip|elss)\b",
    r"\btop\b.*\b(fund|scheme|sip|elss)\b",
    r"\b(buy|sell|hold|exit|invest)\b",
    r"\bwill\b.*\b(rise|fall|grow|drop|return|increase|decrease|outperform|underperform|crash|recover)\b",
]

PII_PATTERNS = [
    r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",            # PAN
    r"\b\d{4}\s?\d{4}\s?\d{4}\b",            # Aadhaar
    r"\b\d{9,18}\b",                          # Bank acct / long numeric
    r"\b\d{6}\b",                             # OTP
    r"[\w\.-]+@[\w\.-]+\.\w+",                # email
    r"\+?\d[\d\s\-]{8,}\d",                   # phone
]


def is_opinion(question: str) -> bool:
    q = question.lower()
    if any(p in q for p in OPINION_PHRASES):
        return True
    return any(re.search(p, q) for p in OPINION_PATTERNS)


def contains_pii(question: str) -> bool:
    return any(re.search(p, question) for p in PII_PATTERNS)

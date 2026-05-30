"""
Beginner Email Spam Classifier
================================
Rule-based weighted keyword scoring — no external libraries needed.
Run: python spam_classifier.py
"""

import re

# --- Spam keyword rules: (pattern, score) ---
SPAM_RULES = [
    (r'\bfree\b',                2.0),
    (r'\bwinner\b',              3.0),
    (r'\bwon\b',                 2.0),
    (r'\bcongratulations\b',     2.0),
    (r'\bclaim\b',               2.0),
    (r'\burgent\b',              2.0),
    (r'\blimited time\b',        3.0),
    (r'\bclick here\b',          3.0),
    (r'\bunsubscribe\b',         1.0),
    (r'\bguaranteed\b',          2.0),
    (r'\bmake money\b',          4.0),
    (r'\bcash\b',                1.5),
    (r'\bprize\b',               3.0),
    (r'\boffer\b',               1.0),
    (r'\bdiscount\b',            1.5),
    (r'\bbuy now\b',             3.0),
    (r'\bact now\b',             3.0),
    (r'\bno cost\b',             2.5),
    (r'\brisk.?free\b',          2.0),
    (r'\bdouble your\b',         3.0),
    (r'\bsecret\b',              1.5),
    (r'\bexclusive deal\b',      2.0),
    (r'\bverify your account\b', 3.0),
    (r'\bsuspended\b',           2.5),
    (r'\bpassword\b',            1.5),
    (r'\blogin\b',               1.0),
]

SPAM_THRESHOLD = 6.0


def score_text(text: str, weight: float = 1.0) -> tuple[float, list[tuple[str, float]]]:
    """Score a piece of text and return (total_score, matched_signals)."""
    total = 0.0
    signals = []

    for pattern, pts in SPAM_RULES:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            earned = pts * weight * len(matches)
            total += earned
            signals.append((matches[0], round(earned, 1)))

    # ALL CAPS words bonus
    caps_words = re.findall(r'\b[A-Z]{3,}\b', text)
    if len(caps_words) > 1:
        earned = len(caps_words) * 0.8 * weight
        total += earned
        signals.append((f"{len(caps_words)} ALL-CAPS word(s)", round(earned, 1)))

    # Excessive exclamation marks
    exclaims = re.findall(r'!+', text)
    if len(exclaims) > 1:
        earned = len(exclaims) * 0.5 * weight
        total += earned
        signals.append((f"{len(exclaims)} exclamation(s)", round(earned, 1)))

    return total, signals


def classify_email(subject: str, body: str) -> dict:
    """
    Classify an email as spam or ham.
    Subject lines are weighted 2× more than the body.
    Returns a result dictionary.
    """
    subject_score, subject_signals = score_text(subject, weight=2.0)
    body_score,    body_signals    = score_text(body,    weight=1.0)

    total_score = subject_score + body_score
    is_spam     = total_score >= SPAM_THRESHOLD
    all_signals = subject_signals + body_signals

    return {
        "verdict":       "SPAM" if is_spam else "HAM (not spam)",
        "total_score":   round(total_score, 1),
        "threshold":     SPAM_THRESHOLD,
        "is_spam":       is_spam,
        "signals":       all_signals,
    }


def print_result(result: dict) -> None:
    """Pretty-print a classification result."""
    emoji  = "🚨" if result["is_spam"] else "✅"
    bar_w  = 30
    filled = int(min(result["total_score"] / (SPAM_THRESHOLD * 2), 1.0) * bar_w)
    bar    = "█" * filled + "░" * (bar_w - filled)

    print("\n" + "─" * 50)
    print(f"  {emoji}  Verdict : {result['verdict']}")
    print(f"     Score  : {result['total_score']} / threshold {result['threshold']}")
    print(f"     [{bar}]")

    if result["signals"]:
        print("\n  Signals detected:")
        for kw, pts in result["signals"]:
            print(f"    • '{kw}'  → +{pts} pts")
    else:
        print("\n  No spam signals found.")
    print("─" * 50 + "\n")


# ─── Demo emails ─────────────────────────────────────────────────────────────

EMAILS = [
    {
        "label":   "Classic spam",
        "subject": "URGENT: You WON a FREE prize!!!",
        "body":    (
            "Congratulations! You have been selected as our winner. "
            "Claim your FREE cash reward now! LIMITED TIME offer — act now "
            "before it expires. Click here to verify your account and double "
            "your prize. Guaranteed satisfaction!"
        ),
    },
    {
        "label":   "Phishing attempt",
        "subject": "Your account has been suspended",
        "body":    (
            "Dear customer, your account was suspended due to suspicious "
            "activity. Please login immediately and verify your password to "
            "restore access. Failure to act now will result in permanent loss."
        ),
    },
    {
        "label":   "Legitimate email",
        "subject": "Team standup notes — Thursday",
        "body":    (
            "Hi everyone, here are the notes from today's standup. "
            "We reviewed the Q3 roadmap and agreed on next sprint priorities. "
            "Let me know if you have any questions. Thanks, Alex"
        ),
    },
    {
        "label":   "Work newsletter",
        "subject": "Monthly product update",
        "body":    (
            "Hello team, this month we shipped the new dashboard, fixed "
            "several bugs reported by customers, and improved load times by 40%. "
            "Next month we'll focus on the mobile app redesign."
        ),
    },
]


def interactive_mode() -> None:
    """Let the user type their own email and classify it."""
    print("\n📧  Enter your own email to classify.")
    print("    (Press Enter twice on a blank line to finish the body)\n")
    subject = input("Subject: ").strip()
    print("Body (blank line to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    body = " ".join(lines)
    result = classify_email(subject, body)
    print_result(result)


def main() -> None:
    print("=" * 50)
    print("   EMAIL SPAM CLASSIFIER — demo run")
    print("=" * 50)

    for email in EMAILS:
        print(f"\n📩  [{email['label']}]")
        print(f"    Subject : {email['subject']}")
        print(f"    Body    : {email['body'][:80]}{'...' if len(email['body']) > 80 else ''}")
        result = classify_email(email["subject"], email["body"])
        print_result(result)

    # Offer interactive mode
    try:
        again = input("Would you like to classify your own email? (y/n): ").strip().lower()
        if again == "y":
            interactive_mode()
    except (KeyboardInterrupt, EOFError):
        pass

    print("\nDone! 👋")


if __name__ == "__main__":
    main()
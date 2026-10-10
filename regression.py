
from collections import Counter

from analyzer import analyze_log, normalize_message


def get_failure_signatures(log_text):
    """Extract and count normalized issues from a log."""
    result = analyze_log(log_text)
    signatures = Counter()

    for issue in result.get("issues", []):
        severity = str(issue.get("severity", "UNKNOWN")).upper()
        message = str(issue.get("message", "")).strip()

        signature = f"{severity}: {normalize_message(message)}"
        signatures[signature] += 1

    return signatures


def compare_regressions(baseline_text, current_text):
    """Compare an older baseline log with a newer regression log."""
    baseline = get_failure_signatures(baseline_text)
    current = get_failure_signatures(current_text)

    new_failures = current - baseline
    resolved_failures = baseline - current

    recurring_failures = Counter({
        signature: min(baseline[signature], current[signature])
        for signature in baseline.keys() & current.keys()
    })

    return {
        "baseline_issue_count": sum(baseline.values()),
        "current_issue_count": sum(current.values()),
        "new_failures": new_failures,
        "resolved_failures": resolved_failures,
        "recurring_failures": recurring_failures,
        "baseline_signatures": baseline,
        "current_signatures": current,
    }

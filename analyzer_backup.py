
import re
from collections import Counter, defaultdict


PATTERNS = {
    "FATAL": re.compile(r"\bFATAL\b", re.IGNORECASE),
    "ERROR": re.compile(
        r"\bERROR\b|\bFAILED\b|\bFAILURE\b", re.IGNORECASE
    ),
    "WARNING": re.compile(
        r"\bWARNING\b|\bWARN\b", re.IGNORECASE
    ),
}

ROOT_CAUSE_RULES = [
    (
        re.compile(r"timeout|timed out", re.IGNORECASE),
        "Timeout or delayed response",
        "Check timeout settings, response delays, and whether "
        "the required event occurred before the deadline.",
    ),
    (
        re.compile(
            r"assertion failed|expected .* received|mismatch",
            re.IGNORECASE,
        ),
        "Assertion or data mismatch",
        "Compare expected and actual values, inspect the test "
        "inputs, and review the logic producing the result.",
    ),
    (
        re.compile(r"memory|out of memory|allocation", re.IGNORECASE),
        "Possible memory-related issue",
        "Inspect memory allocation, resource limits, and the "
        "surrounding log messages.",
    ),
    (
        re.compile(
            r"permission denied|access denied|unauthorized",
            re.IGNORECASE,
        ),
        "Possible permissions issue",
        "Verify account permissions, file access, and relevant "
        "configuration.",
    ),
    (
        re.compile(
            r"connection refused|connection failed|network error",
            re.IGNORECASE,
        ),
        "Possible connection issue",
        "Check endpoint configuration, service availability, "
        "network connectivity, and connection settings.",
    ),
    (
        re.compile(r"link training", re.IGNORECASE),
        "Link training did not complete successfully",
        "Inspect link-training events, initialization sequence, "
        "timeout settings, and preceding error messages.",
    ),
]


def normalize_message(message):
    """Normalize variable values to group similar log messages."""
    message = message.strip().lower()
    message = re.sub(r"\b0x[0-9a-f]+\b", "<hex>", message)
    message = re.sub(r"\b\d+\b", "<n>", message)
    message = re.sub(r"\s+", " ", message)
    return message


def analyze_log(log_text, context_lines=2):
    """Analyze engineering logs and investigate possible failure causes."""

    lines = log_text.splitlines()
    issues = []
    groups = defaultdict(list)

    for line_number, line in enumerate(lines, start=1):
        severity = None

        for level in ("FATAL", "ERROR", "WARNING"):
            if PATTERNS[level].search(line):
                severity = level
                break

        if severity is None:
            continue

        issue = {
            "line": line_number,
            "severity": severity,
            "message": line.strip(),
        }
        issues.append(issue)

        key = (severity, normalize_message(line))
        groups[key].append(issue)

    grouped_failures = []

    for (severity, normalized), occurrences in groups.items():
        grouped_failures.append({
            "severity": severity,
            "pattern": normalized,
            "count": len(occurrences),
            "lines": [item["line"] for item in occurrences],
            "example": occurrences[0]["message"],
        })

    grouped_failures.sort(
        key=lambda item: (
            {"FATAL": 0, "ERROR": 1, "WARNING": 2}[item["severity"]],
            -item["count"],
        )
    )

    investigations = []

    for issue in issues:
        matched = False

        for pattern, title, recommendation in ROOT_CAUSE_RULES:
            if pattern.search(issue["message"]):
                start = max(0, issue["line"] - 1 - context_lines)
                end = min(
                    len(lines),
                    issue["line"] + context_lines,
                )

                investigations.append({
                    "line": issue["line"],
                    "severity": issue["severity"],
                    "message": issue["message"],
                    "possible_cause": title,
                    "evidence": lines[start:end],
                    "recommendation": recommendation,
                    "confidence": "Rule-based hypothesis; verify manually",
                })
                matched = True
                break

        if not matched and issue["severity"] in ("FATAL", "ERROR"):
            start = max(0, issue["line"] - 1 - context_lines)
            end = min(len(lines), issue["line"] + context_lines)

            investigations.append({
                "line": issue["line"],
                "severity": issue["severity"],
                "message": issue["message"],
                "possible_cause": "Undetermined from available log evidence",
                "evidence": lines[start:end],
                "recommendation": (
                    "Inspect surrounding events and relevant test "
                    "configuration before determining the cause."
                ),
                "confidence": "Insufficient evidence",
            })

    counts = Counter(item["severity"] for item in issues)

    return {
        "total_lines": len(lines),
        "total_issues": len(issues),
        "counts": dict(counts),
        "issues": issues,
        "groups": grouped_failures,
        "investigations": investigations,
        "first_failure": issues[0] if issues else None,
    }


import json
import streamlit as st
import pandas as pd

from analyzer import analyze_log
from regression import compare_regressions

st.set_page_config(
    page_title="TraceMind AI",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 TraceMind AI")
st.caption(
    "AI-Powered Engineering Log Investigator | "
    "Rule-based log analysis and regression comparison"
)

analysis_tab, regression_tab = st.tabs([
    "📄 Log Investigation",
    "🔬 Regression Comparison"
])


def read_log(uploaded_file):
    return uploaded_file.getvalue().decode(
        "utf-8",
        errors="replace"
    )


def display_failures(title, failures, empty_message):
    st.subheader(title)

    if not failures:
        st.info(empty_message)
        return

    for signature, count in failures.items():
        st.write(f"**Occurrences: {count}** — {signature}")


with analysis_tab:
    st.header("Engineering Log Investigation")

    uploaded_file = st.file_uploader(
        "Upload an engineering log",
        type=["log", "txt"],
        key="single_log"
    )

    context_lines = st.slider(
        "Context lines around issues",
        min_value=1,
        max_value=10,
        value=3
    )

    use_demo = st.button("Load Demo Log")

    if uploaded_file is not None:
        log_text = read_log(uploaded_file)

    elif use_demo:
        try:
            with open("demo.log", "r", encoding="utf-8") as file:
                log_text = file.read()
        except FileNotFoundError:
            log_text = ""
            st.error("demo.log was not found in the project folder.")
    else:
        log_text = ""

    if log_text:
        result = analyze_log(
            log_text,
            context_lines=context_lines
        )

        st.subheader("Analysis Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Lines",
            result["total_lines"]
        )

        col2.metric(
            "Total Issues",
            result["total_issues"]
        )

        col3.metric(
            "Issue Types",
            len(result.get("groups", []))
        )

        counts = result.get("counts", {})

        if counts:
            st.subheader("Issue Severity")

            chart_data = pd.DataFrame({
                "Severity": list(counts.keys()),
                "Count": list(counts.values())
            })

            st.bar_chart(
                chart_data.set_index("Severity")
            )

        first_failure = result.get("first_failure")

        if first_failure:
            st.subheader("First Detected Issue")

            st.write(
                f"**Line:** {first_failure['line']}"
            )

            st.write(
                f"**Severity:** {first_failure['severity']}"
            )

            st.code(first_failure["message"])

        groups = result.get("groups", [])

        if groups:
            st.subheader("Repeated Issue Patterns")

            groups_df = pd.DataFrame(groups)

            st.dataframe(
                groups_df,
                use_container_width=True,
                hide_index=True
            )

        # Corrected root-cause investigation display
        investigations = result.get("investigations", [])

        if investigations:
            st.subheader("Root-Cause Investigations")

            for index, item in enumerate(
                investigations,
                start=1
            ):
                possible_cause = item.get(
                    "possible_cause",
                    "Undetermined possible cause"
                )

                severity = item.get("severity", "ISSUE")
                line_number = item.get("line", "?")

                with st.expander(
                    f"{index}. {severity} | Line {line_number} | "
                    f"{possible_cause}"
                ):
                    st.write("**Original log message**")

                    st.code(
                        item.get(
                            "message",
                            "No message available"
                        ),
                        language="text"
                    )

                    st.write("**Possible cause**")
                    st.write(possible_cause)

                    st.write("**Confidence**")

                    st.caption(
                        item.get(
                            "confidence",
                            "Rule-based hypothesis; verify manually"
                        )
                    )

                    evidence = item.get("evidence", [])

                    if evidence:
                        st.write("**Surrounding log evidence**")

                        st.code(
                            "\n".join(evidence),
                            language="text"
                        )

                    recommendation = item.get("recommendation")

                    if recommendation:
                        st.write("**Recommended next step**")
                        st.write(recommendation)

        else:
            st.info(
                "No root-cause investigations were generated. "
                "Try a log containing errors, failures, or known "
                "warning patterns."
            )

        st.subheader("Export Results")

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "Download Analysis as JSON",
                data=json.dumps(
                    result,
                    indent=2,
                    default=str
                ),
                file_name="tracemind_analysis.json",
                mime="application/json",
                use_container_width=True
            )

        with col2:
            st.download_button(
                "Download Original Log",
                data=log_text,
                file_name="engineering_log.log",
                mime="text/plain",
                use_container_width=True
            )

        with st.expander("View Complete Log"):
            st.text(log_text)

    else:
        st.info(
            "Upload a .log or .txt file, or click Load Demo Log "
            "to start an investigation."
        )


with regression_tab:
    st.header("Regression Comparison Engine")

    st.write(
        "Compare a baseline log against a newer log to identify "
        "new, resolved, and recurring issue patterns."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Baseline Log")

        baseline_file = st.file_uploader(
            "Upload the older log",
            type=["log", "txt"],
            key="baseline_log"
        )

    with col2:
        st.subheader("Current Log")

        current_file = st.file_uploader(
            "Upload the newer log",
            type=["log", "txt"],
            key="current_log"
        )

    if st.button(
        "Compare Regression Logs",
        type="primary"
    ):
        if baseline_file is None or current_file is None:
            st.warning(
                "Please upload both the baseline and current log files."
            )

        else:
            baseline_text = read_log(baseline_file)
            current_text = read_log(current_file)

            comparison = compare_regressions(
                baseline_text,
                current_text
            )

            st.subheader("Comparison Summary")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Baseline Issues",
                comparison["baseline_issue_count"]
            )

            current_delta = (
                comparison["current_issue_count"]
                - comparison["baseline_issue_count"]
            )

            col2.metric(
                "Current Issues",
                comparison["current_issue_count"],
                delta=current_delta,
                delta_color="inverse"
            )

            col3.metric(
                "New Failure Patterns",
                len(comparison["new_failures"])
            )

            display_failures(
                "🆕 New Failures",
                comparison["new_failures"],
                "No new failure patterns detected."
            )

            display_failures(
                "✅ Resolved Failures",
                comparison["resolved_failures"],
                "No previously detected patterns were resolved."
            )

            display_failures(
                "🔁 Recurring Failures",
                comparison["recurring_failures"],
                "No recurring failure patterns detected."
            )

            report = {
                "baseline_issue_count":
                    comparison["baseline_issue_count"],

                "current_issue_count":
                    comparison["current_issue_count"],

                "new_failures":
                    dict(comparison["new_failures"]),

                "resolved_failures":
                    dict(comparison["resolved_failures"]),

                "recurring_failures":
                    dict(comparison["recurring_failures"])
            }

            st.download_button(
                "Download Regression Report",
                data=json.dumps(report, indent=2),
                file_name="tracemind_regression_report.json",
                mime="application/json"
            )

st.divider()

st.caption(
    "TraceMind AI | Demonstration prototype. "
    "Validate findings against real engineering logs."
)

# TraceMind-AI — Engineering Log Investigator

**A Python-based tool for engineering log analysis, failure investigation, and regression detection.**

TraceMind-AI analyzes simulation and system logs to identify errors, warnings, and fatal events. It groups repeated failure patterns, presents surrounding log evidence, suggests possible causes using predefined rules, and compares baseline logs with current logs to identify new, resolved, and recurring failures.

The project is designed as an educational prototype for exploring debugging and verification workflows.

## Features

- **Log Analysis:** Upload `.log` and `.txt` files for analysis.
- **Severity Detection:** Identify `FATAL`, `ERROR`, `WARNING`, `FAILED`, and `FAILURE` messages.
- **Failure Grouping:** Group similar messages and count repeated occurrences.
- **Root-Cause Hypotheses:** Generate preliminary troubleshooting suggestions based on predefined rules.
- **Evidence Inspection:** Display surrounding log lines to help investigate failures.
- **Regression Comparison:** Compare baseline and current logs to identify new, resolved, and recurring failure patterns.
- **Interactive Dashboard:** View issue counts, severity summaries, and investigation details.
- **Report Export:** Download analysis and regression results.
- **No API Key Required:** Run the current version without an external AI service.

## Technology Stack

- Python
- Streamlit
- Pandas
- Regular expressions
- Python `unittest`

## Project Structure

```text
TraceMind-AI/
├── app.py
├── analyzer.py
├── regression.py
├── test_regression.py
├── demo.log
├── baseline.log
├── requirements.txt
├── README.md
└── .gitignore
```

## Prerequisites

- Python 3.10 or later
- pip

## Installation

Clone your repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TraceMind-AI
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## How to Use

1. Launch the application.
2. Use the demo option or upload a `.log` or `.txt` file.
3. Review detected issues, severity counts, and repeated failure patterns.
4. Expand investigation results to inspect possible causes, supporting log evidence, and troubleshooting recommendations.
5. Open the regression comparison section.
6. Compare a baseline log against a current log.
7. Review new, resolved, and recurring failure patterns.
8. Download the available reports for further analysis.

## Run Automated Tests

Run the regression tests with:

```bash
python -m unittest test_regression.py -v
```

The tests check whether the comparison logic identifies new, resolved, and recurring failure patterns.

## Current Limitations

- Failure detection and root-cause hypotheses use predefined text patterns and rules.
- Suggested causes are not guaranteed to be correct and require manual verification.
- Regression matching uses normalized log messages; semantically equivalent messages may not always match.
- The current prototype does not connect to real hardware or execute RTL simulations.
- LLM-based analysis and machine-learning-based root-cause prediction are not implemented.

## Future Enhancements

- LLM-assisted investigation with evidence-grounded explanations.
- Timestamp-based event correlation and failure sequence analysis.
- Engineering protocol-specific rules and configurable log formats.
- Additional automated tests and regression metrics.
- Interactive investigation timelines and richer report exports.

## Disclaimer

TraceMind-AI is an educational prototype. Its findings and troubleshooting suggestions must be validated by a qualified engineer before being used for engineering decisions.

## Author

Developed as a Python engineering log analysis and regression detection project.
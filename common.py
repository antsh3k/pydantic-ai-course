"""
Common functions and classes for the SQL agent.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from pydantic_ai import ModelRetry, RunContext
from pydantic_evals.reporting import EvaluationReport
from tabulate import tabulate

load_dotenv()

_REPO_ROOT = Path(__file__).resolve().parent
_SESSION4_PRODUCT_NAMING_BRIEFS_PATH = _REPO_ROOT / "session4_product_naming_briefs.json"


### Used in Session 4 Parts 1-4 ###
@dataclass
class DbDeps:
    """
    Part of our mock database - a dictionary of table name: list of column names.
    """

    tables: Dict[str, List[str]]


def run_sql_query(ctx: RunContext[DbDeps], sql: str) -> str:
    """
    Execute a SQL query against the database.

    This is a read-only environment - only SELECT queries are allowed.
    """
    if "drop" in sql.lower() or "delete" in sql.lower():
        raise ModelRetry("DROP or DELETE operations are not allowed. This is a read-only environment.")

    try:
        result = run_query(ctx.deps.tables, sql)
        return str(result)
    except Exception as e:
        error_msg = str(e)
        if "does not exist" in error_msg:
            available_tables = ", ".join(ctx.deps.tables.keys())
            raise ModelRetry(
                f"{error_msg} Please check the table name and try again. Available tables: {available_tables}"
            )
        return error_msg


def run_query(fake_database: Dict[str, List[str]], sql: str) -> list[tuple[int, Any]]:
    """
    Execute a fake SQL query against the database.

    This is a read-only environment - only SELECT queries are allowed.
    Use this tool to "retrieve data" from available tables.
    """
    match = re.search(r"FROM\s+(\w+)", sql, re.IGNORECASE)

    if match:
        table_name = match.group(1)
        if table_name not in fake_database:
            raise Exception(f"Error: Table '{table_name}' does not exist. ")

        # Mock execution - return sample data instead of actually running the query against a database
        if "users" in sql.lower():
            return [(1, "alice@example.com"), (2, "bob@example.com")]
        elif "orders" in sql.lower():
            return [(1, 99.99), (2, 149.50)]
        else:
            raise Exception(f"Couldn't retrieve data from table {table_name}.")
    else:
        raise Exception("Error: Invalid SQL query. Please use a SELECT statement.")


### Used in Session 4 Part 5 ###
def load_session4_product_naming_briefs() -> list[dict[str, str]]:
    """Return ordered rows ``{brief_name, brief_text}`` from the Session 4 Part 5 JSON file."""
    with _SESSION4_PRODUCT_NAMING_BRIEFS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def scores_to_table(
    reports_by_pass: list[EvaluationReport[Any, Any, Any]],
    brief_names_ordered: list[str],
    *,
    score_key: str = "naming_judge",
) -> str:
    """
    Build a score table reporting on student performance.
    Used in Session 4 Part 5.
    """
    rows: list[list[str | int]] = []
    for pass_idx, report in enumerate(reports_by_pass):
        by_brief: dict[str, str] = {}
        for rc in report.cases:
            key = rc.name or ""
            er = rc.scores.get(score_key)
            if er is None:
                by_brief[key] = "n/a"
            else:
                try:
                    value = float(er.value)
                    by_brief[key] = f"{value:.1f}" if math.isfinite(value) else "n/a"
                except (TypeError, ValueError):
                    by_brief[key] = "n/a"
        rows.append([pass_idx, *[by_brief.get(col, "n/a") for col in brief_names_ordered]])

    headers = ["pass", *brief_names_ordered]
    return tabulate(rows, headers=headers, tablefmt="github")

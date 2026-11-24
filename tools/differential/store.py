import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from tools.differential.runner import Comparison

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "db" / "schema.sql"


def persist(database: Path, version: str, seed: int, comparisons: list[Comparison]) -> int:
    recorded_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    mismatches = sum(not comparison.matched for comparison in comparisons)
    connection = sqlite3.connect(database)
    try:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        connection.execute("PRAGMA foreign_keys = ON")
        with connection:
            cursor = connection.execute(
                "INSERT INTO differential_run "
                "(project_version, seed, case_count, mismatch_count, recorded_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (version, seed, len(comparisons), mismatches, recorded_at),
            )
            run_id = cursor.lastrowid
            connection.executemany(
                "INSERT INTO differential_case "
                "(run_id, case_index, category, input_sha256, expected_exit, python_exit, java_exit, matched) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        run_id,
                        comparison.index,
                        comparison.case.category,
                        comparison.input_sha256,
                        comparison.case.expected_exit,
                        comparison.python.exit_code,
                        comparison.java.exit_code,
                        int(comparison.matched),
                    )
                    for comparison in comparisons
                ],
            )
        return run_id
    finally:
        connection.close()

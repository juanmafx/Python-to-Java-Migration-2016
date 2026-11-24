import sqlite3
from pathlib import Path

import pytest

from tools.differential.corpus import Case
from tools.differential.runner import Comparison, Outcome
from tools.differential.store import SCHEMA_PATH, persist


@pytest.fixture
def connection():
    database = sqlite3.connect(":memory:")
    database.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    database.execute("PRAGMA foreign_keys = ON")
    yield database
    database.close()


def insert_run(database, case_count=1, mismatch_count=0):
    return database.execute(
        "INSERT INTO differential_run (project_version, seed, case_count, mismatch_count, recorded_at) "
        "VALUES ('1.0.0', 1, ?, ?, '2026-11-23T00:00:00Z')",
        (case_count, mismatch_count),
    ).lastrowid


def test_schema_is_idempotent(connection):
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def test_rejects_more_mismatches_than_cases(connection):
    with pytest.raises(sqlite3.IntegrityError):
        insert_run(connection, case_count=1, mismatch_count=2)


def test_rejects_case_without_run(connection):
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "INSERT INTO differential_case VALUES (99, 0, 'random', ?, 0, 0, 0, 1)", ("a" * 64,)
        )


def test_rejects_malformed_digest(connection):
    run_id = insert_run(connection)
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "INSERT INTO differential_case VALUES (?, 0, 'random', ?, 0, 0, 0, 1)", (run_id, "Z" * 64)
        )


def test_deleting_a_run_cascades(connection):
    run_id = insert_run(connection)
    connection.execute(
        "INSERT INTO differential_case VALUES (?, 0, 'random', ?, 0, 0, 0, 1)", (run_id, "a" * 64)
    )
    connection.execute("DELETE FROM differential_run WHERE id = ?", (run_id,))
    assert connection.execute("SELECT COUNT(*) FROM differential_case").fetchone() == (0,)


def test_persist_stores_digest_and_never_raw_input(tmp_path: Path):
    payload = b"1\n2\n"
    outcome = Outcome(b"X = 3\n", b"", 0)
    case = Case("random", payload, outcome.stdout, outcome.stderr, outcome.exit_code)
    database = tmp_path / "runs.sqlite3"
    run_id = persist(database, "1.0.0", 5, [Comparison(0, case, outcome, outcome)])
    stored = sqlite3.connect(database)
    try:
        row = stored.execute(
            "SELECT category, input_sha256, matched FROM differential_case WHERE run_id = ?", (run_id,)
        ).fetchone()
    finally:
        stored.close()
    assert row[0] == "random" and len(row[1]) == 64 and row[2] == 1

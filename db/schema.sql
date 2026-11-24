-- Optional SQLite 3.37+ schema for differential run results.
-- The solvers never touch it; only `python -m tools.differential --database` writes here.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS differential_run (
    id INTEGER PRIMARY KEY,
    project_version TEXT NOT NULL CHECK (length(project_version) BETWEEN 1 AND 32),
    seed INTEGER NOT NULL,
    case_count INTEGER NOT NULL CHECK (case_count >= 0),
    mismatch_count INTEGER NOT NULL CHECK (mismatch_count BETWEEN 0 AND case_count),
    recorded_at TEXT NOT NULL CHECK (recorded_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T*Z')
) STRICT;

CREATE TABLE IF NOT EXISTS differential_case (
    run_id INTEGER NOT NULL REFERENCES differential_run (id) ON DELETE CASCADE,
    case_index INTEGER NOT NULL CHECK (case_index >= 0),
    category TEXT NOT NULL CHECK (category IN ('boundary', 'random', 'formatting', 'invalid')),
    input_sha256 TEXT NOT NULL CHECK (length(input_sha256) = 64 AND input_sha256 NOT GLOB '*[^0-9a-f]*'),
    expected_exit INTEGER NOT NULL,
    python_exit INTEGER NOT NULL,
    java_exit INTEGER NOT NULL,
    matched INTEGER NOT NULL CHECK (matched IN (0, 1)),
    PRIMARY KEY (run_id, case_index)
) STRICT, WITHOUT ROWID;

CREATE INDEX IF NOT EXISTS idx_differential_case_mismatch
    ON differential_case (run_id, category)
    WHERE matched = 0;

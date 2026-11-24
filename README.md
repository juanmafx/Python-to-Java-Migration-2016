# Python-to-Java-Migration-2016

A small, rigorously verified case study in migrating a program from Python to Java without changing its behavior. Both implementations solve one integer-sum problem, and a differential test harness proves they agree.

> **Project history:** originally created in 2017 (first commit 2017-09-21), modernized in 2026. The repository name keeps its original "2016" label.

## Purpose

The program reads two integers from standard input and prints their sum as `X = <sum>`. The task is URI Online Judge problem 1001, "Extremely Basic" (the judge is now named beecrowd). The problem belongs to its authors; see [NOTICE](NOTICE).

## Why this project exists

It began as a study exercise: solve the same problem in two languages. The arithmetic is trivial, which makes the migration risk easy to see. The original pair looked equivalent but was not:

| Input | Original Python | Original Java |
| --- | --- | --- |
| `2147483647` and `1` | `X = 2147483648` | `X = -2147483648` (silent overflow) |
| `1 2` on one line | crash | `X = 3` |
| `1_0` and `2` | `X = 12` | crash |

Version 1.0.0 defines one explicit input contract, implements it in both languages, and tests the two against each other.

## What it does

- Adds integers of up to 4,096 digits with no overflow.
- Accepts operands separated by any mix of space, tab, CR, or LF.
- Accepts only ASCII operands matching `[+-]?[0-9]+`.
- Rejects invalid input with exit code `2` and a stable error code on standard error. Input is never echoed.

| Error code | Meaning |
| --- | --- |
| `input_too_large` | Input exceeds 16,384 bytes |
| `wrong_operand_count` | Input does not contain exactly two tokens |
| `invalid_operand` | A token is not a signed ASCII decimal integer |
| `operand_too_long` | An operand has more than 4,096 digits |

## Architecture

```text
python/src/integer_sum/   Reference implementation (core and CLI)
java/src/main/java/...    Java port with the same module boundaries
tools/differential/       Seeded corpus, process runner, optional SQLite store
tools/reporting/          Builds reports/tests/ from real test output
db/schema.sql             Optional schema for differential run results
reports/tests/            Committed report from an actual run
```

There is no frontend or server. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the design and complexity analysis.

## Quick start

Requirements: Python 3.14+, JDK 17+, and Maven 3.9+.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install ./python
printf '10\n9\n' | .venv/bin/integer-sum

mvn -q -f java/pom.xml -DskipTests package
printf '10 9' | java -jar java/target/integer-sum-1.0.0.jar
```

Both commands print `X = 19`.

## Usage guide

```bash
$ printf '2147483647\n1\n' | java -jar java/target/integer-sum-1.0.0.jar
X = 2147483648

$ printf 'abc 1' | .venv/bin/integer-sum
error: invalid_operand

$ echo $?
2
```

Compare both implementations on a reproducible corpus:

```bash
.venv/bin/python -m pip install --require-hashes -r python/requirements-dev.txt
mvn -q -f java/pom.xml compile
PYTHONPATH=python/src .venv/bin/python -m tools.differential --seed 20260101 --database runs.sqlite3
```

## Configuration

The solvers take no configuration, environment variables, or secrets. Their limits are constants in `core/parsing.py` and `OperandParser.java`.

| Differential option | Default | Purpose |
| --- | --- | --- |
| `--seed` | `20260101` | Seed for the generated corpus |
| `--random-cases` | `200` | Generated cases added to the fixed ones |
| `--workers` | `4` | Concurrent case runners |
| `--output` | none | JSON summary path |
| `--database` | none | Optional SQLite results path |

## Database (optional)

The solvers have no persistence and do not need a database. [db/schema.sql](db/schema.sql) is an optional SQLite schema that stores differential run results when `--database` is passed. It stores SHA-256 digests of inputs rather than the inputs.

## Testing

```bash
PYTHON=.venv/bin/python scripts/run-tests.sh
```

The script runs:

- Python unit, CLI, schema, and corpus tests with pytest.
- Property-based tests with Hypothesis (derandomized) and jqwik (fixed seed).
- A chi-square uniformity check on the corpus generator.
- Java unit and CLI tests with JUnit 5.
- The cross-language differential run.

The latest results are in [reports/tests/TEST_REPORT.md](reports/tests/TEST_REPORT.md).

## Security notes

Input size and operand length are bounded before conversion, errors never reflect input, and CI runs with read-only permissions and pinned actions. See [SECURITY.md](SECURITY.md) and [docs/SECURITY_AUDIT.md](docs/SECURITY_AUDIT.md).

## License and attribution

Licensed under the [Apache License 2.0](LICENSE). The problem statement is third-party material and is credited in [NOTICE](NOTICE).

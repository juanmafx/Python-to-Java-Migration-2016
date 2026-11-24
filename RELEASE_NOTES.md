# Release Notes: 1.0.0

First versioned release, prepared in 2026 from study code first committed in 2017. No tag or GitHub release has been created yet.

## Highlights

- Python and Java now follow one written input contract.
- Java no longer overflows; both versions handle operands of up to 4,096 digits.
- Invalid input yields a stable error code and exit status `2` instead of a stack trace.
- A seeded differential harness compares both implementations process by process.

## Breaking changes

- Files moved to `python/` and `java/`.
- Inputs such as `1_0` and non-ASCII digits are now rejected.
- Python now accepts two operands on one line, matching the Java behavior.

## Verification

Run `scripts/run-tests.sh`. Results from the run made for this release are in `reports/tests/TEST_REPORT.md`.

# Security Audit

Audit dates: 2026-11-23 and 2026-11-24. Scope: the working tree of version 1.0.0 and the full git history of this repository. Tool results reflect advisory data on the audit date and are not a guarantee that no vulnerabilities exist.

## Findings fixed

| ID | Weakness | Original impact | Fix |
| --- | --- | --- | --- |
| SA-1 | CWE-190 integer overflow | Java returned a wrong sum beyond 32 bits | `BigInteger` arithmetic |
| SA-2 | CWE-400 uncontrolled resource use | Input size and digit count were unbounded | Bounded read and digit limit |
| SA-3 | CWE-20 improper input validation | Runtimes accepted different numeric forms | One strict ASCII grammar |
| SA-4 | CWE-209 error message exposure | Crashes printed stack traces | Fixed error codes with no input echo |
| SA-5 | CWE-248 uncaught exception | A low `PYTHONINTMAXSTRDIGITS` crashed Python on valid input | CLI sets its own conversion limit |
| SA-6 | CWE-391 unchecked error condition | Java exited `0` after a failed write, losing the result | Direct output stream, exit `3` |
| SA-7 | CWE-248 uncaught exception | Read and write failures printed tracebacks | Stable `io_failure` error |
| SA-8 | CWE-1395 vulnerable component | Build backend setuptools 80.9.0 had PYSEC-2026-3447 and GHSA-xmj3-9gf7-h52w | Raised to 84.2.1 |
| SA-9 | CWE-1395 vulnerable component | Maven plugins loaded `plexus-utils` 3.6.0 and 4.0.2 with GHSA-6fmv-xxpf-w3cw | Raised to 3.6.1 and 4.0.3 |
| SA-10 | CWE-20 improper input validation | Out-of-range differential options caused tracebacks or were silently accepted | Validated at argument parsing |

SA-8 and SA-9 affect the build only. The solvers have no runtime dependencies.

## Checks performed

| Check | Result |
| --- | --- |
| `pip-audit` on the hash-locked Python test dependencies | No known vulnerabilities |
| `pip-audit` on the pinned build backend | No known vulnerabilities |
| OSV query for all 59 JAR artifacts resolved by `mvn clean verify`, including plugins | No advisories |
| `gitleaks --redact` on the full history and the working tree | No findings |
| `zizmor` on the CI workflow, offline | No findings at the default persona |
| Injection and unsafe evaluation review | No shell, dynamic evaluation, or deserialization |
| XSS, CSRF, authentication, and 2FA review | Not applicable: no web surface, accounts, or stored credentials |
| Cryptography review | SHA-256 is used only to fingerprint corpus inputs, not for secrecy |
| SQL review of the differential store | All values use bound parameters |

## Hardening

- The CI workflow uses read-only `contents` permission, commit-pinned actions, and no persisted checkout credentials. It had not yet run on GitHub at the audit date.
- Python test dependencies are installed with `--require-hashes`. The build backend is pinned by version only.
- Maven dependencies and plugins use fixed versions.
- The optional database stores input digests instead of raw inputs.

## Open items

No code-level findings are open. The process-level differences for unusual standard input are listed under Known limitations in [ARCHITECTURE.md](ARCHITECTURE.md). Two items remain in existing git history and cannot be changed without rewriting it:

- Earlier commits contain the original source, including the verbatim third-party problem statement.
- Commit metadata contains author email addresses that are not GitHub noreply addresses.

# Security Audit

Audit date: 2026-11-23. Scope: the working tree of version 1.0.0 and the full git history of this repository.

## Findings fixed

| ID | Weakness | Original impact | Fix |
| --- | --- | --- | --- |
| SA-1 | CWE-190 integer overflow | Java returned a wrong sum beyond 32 bits | `BigInteger` arithmetic |
| SA-2 | CWE-400 uncontrolled resource use | Input size and digit count were unbounded | Bounded read and digit limit |
| SA-3 | CWE-20 improper input validation | Runtimes accepted different numeric forms | One strict ASCII grammar |
| SA-4 | CWE-209 error message exposure | Crashes printed stack traces | Fixed error codes with no input echo |

## Checks performed

| Check | Result |
| --- | --- |
| `pip-audit` on the hash-locked Python test dependencies | No known vulnerabilities |
| OSV query for all 13 resolved Maven test dependencies | No advisories |
| Pattern search of full history for private keys and common credentials | No matches |
| Injection, XSS, CSRF, and unsafe evaluation review | Not applicable to the solvers: no web surface, shell, or dynamic evaluation |
| SQL review of the differential store | All values use bound parameters |

The solvers have no runtime dependencies. Dependency results reflect advisory data on the audit date.

## Hardening

- CI uses read-only `contents` permission, commit-pinned actions, and no persisted checkout credentials.
- Python test dependencies are installed with `--require-hashes`.
- Maven dependencies and plugins use fixed versions.
- The optional database stores input digests instead of raw inputs.

## Open items

No code-level findings are open. Two items remain in existing git history and cannot be changed without rewriting it:

- Earlier commits contain the original source, including the verbatim third-party problem statement.
- Commit metadata contains author email addresses that are not GitHub noreply addresses.

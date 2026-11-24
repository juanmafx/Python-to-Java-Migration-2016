# Security Policy

## Supported versions

| Version | Supported |
| --- | --- |
| 1.x | Yes |
| Earlier unversioned code | No |

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting for this repository if it is available. If it is not, open an issue asking for a private contact and leave out any technical detail.

This is a personal project maintained on a best-effort basis, so no response time is guaranteed.

## Security model

The solvers read untrusted bytes from standard input and use no network, credentials, or files. The differential tool is a development tool: it starts the Python and Java solvers as subprocesses without a shell, and it writes only to the `--output` and `--database` paths an operator passes.

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

The tools read untrusted bytes from standard input. They use no network, credentials, or files, except the optional SQLite path an operator passes to the differential tool.

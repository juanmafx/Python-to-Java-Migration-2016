# Changelog

This project follows [Semantic Versioning](https://semver.org/).

## [1.0.0] - Unreleased

### Added

- Layered Python package and Java 17 Maven project.
- Unit, CLI, property-based, statistical, and cross-language differential tests.
- Optional SQLite schema for differential run results.
- Generated test report, GitHub Actions CI, and security and architecture documentation.

### Changed

- **Breaking:** both implementations now share one strict input contract.
- **Breaking:** invalid input now exits with code `2` and a stable error code.
- **Breaking:** read and write failures now exit with code `3` and `error: io_failure`.
- Source files moved from `1001-Python` and `1001-Java` into `python/` and `java/`.
- All identifiers and documentation are in English.

### Fixed

- Java integer overflow beyond 32 bits.
- Unbounded input handling.
- Parsing differences between the two implementations.
- Python crash on valid input when `PYTHONINTMAXSTRDIGITS` was set below the operand limit.
- Java reporting success after a failed write to standard output.
- Tracebacks from the differential tool on out-of-range options.

### Security

- Build backend raised to setuptools 84.2.1 to resolve PYSEC-2026-3447 and GHSA-xmj3-9gf7-h52w.
- `plexus-utils` on the Maven plugin classpath raised to 3.6.1 and 4.0.3 to resolve GHSA-6fmv-xxpf-w3cw.

### Removed

- The verbatim third-party problem statement from the working tree.

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
- Source files moved from `1001-Python` and `1001-Java` into `python/` and `java/`.
- All identifiers and documentation are in English.

### Fixed

- Java integer overflow beyond 32 bits.
- Unbounded input handling.
- Parsing differences between the two implementations.

### Removed

- The verbatim third-party problem statement from the working tree.

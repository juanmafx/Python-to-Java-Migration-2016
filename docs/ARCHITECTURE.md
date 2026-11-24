# Architecture

## Goals

1. One written input contract, implemented identically in two languages.
2. Pure core logic, with all I/O at the edge.
3. Equivalence established by execution rather than by reading the code.

## Module structure

```text
.
|-- python/
|   |-- src/integer_sum/
|   |   |-- core/        errors, parsing, solver
|   |   `-- cli/         stream wiring and exit codes
|   `-- tests/
|-- java/
|   `-- src/
|       |-- main/java/io/github/juanmafx/integersum/
|       |   |-- core/    InputErrorCode, InvalidInputException, Operands, OperandParser, Solver
|       |   `-- cli/     Application
|       `-- test/
|-- tools/
|   |-- differential/    corpus, runner, store, entry point
|   `-- reporting/       report builder
|-- db/schema.sql
`-- reports/tests/
```

The project is a command-line tool, so it has no `frontend/` or `backend/` split.

## Data flow

```text
stdin (bounded read) -> tokenize -> validate -> add -> render -> stdout
                                       |
                                       `-> typed error -> stderr, exit 2
```

## Module mapping

| Responsibility | Python | Java |
| --- | --- | --- |
| Error codes | `core/errors.py` | `InputErrorCode`, `InvalidInputException` |
| Parsing and limits | `core/parsing.py` | `OperandParser` |
| Arithmetic and output | `core/solver.py` | `Solver` |
| Process boundary | `cli/app.py` | `Application` |

## Migration decisions

| Concern | Original behavior | Decision |
| --- | --- | --- |
| Integer width | Python unbounded, Java 32-bit | `BigInteger` in Java |
| Separators | Python line-based, Java any Unicode whitespace | Space, tab, CR, LF in both |
| Digit grammar | Each runtime's own rules, including non-ASCII digits | ASCII `[+-]?[0-9]+` in both |
| Underscores | Accepted by Python only | Rejected in both |
| Failure mode | Uncaught exception and stack trace | Typed error code, exit 2 |
| Line ending | Platform-dependent in Java `println` | Always LF |

## Complexity

Let `d` be the larger operand's digit count and `n` the input size in bytes.

| Step | Time | Space |
| --- | --- | --- |
| Bounded read and tokenization | `O(n)` | `O(n)` |
| Grammar validation | `O(d)` | `O(1)` extra |
| Decimal to binary conversion | at most `O(d^2)` | `O(d)` |
| Addition | `O(d)` | `O(d)` |
| Binary to decimal rendering | at most `O(d^2)` | `O(d)` |

Decimal conversion dominates. The limits `n <= 16,384` and `d <= 4,096` turn that superlinear cost into a fixed upper bound. The digit limit also stays below CPython's default 4,300-digit conversion guard, so both runtimes accept the same inputs.

## Verification strategy

- **Example tests** pin the contract, including each error code and limit.
- **Property tests** check commutativity, associativity, identity, decimal round trips, and that arbitrary bytes produce either a result or a typed error.
- **Differential tests** run both executables as separate processes and compare stdout, stderr, and exit code with an expected value from the corpus generator.
- **Statistical test** applies a chi-square goodness-of-fit check (63 degrees of freedom, alpha 0.001) to the generator's digit-length distribution.

The corpus combines all pairs of 32-bit and 64-bit boundary values, maximum-width operands, malformed inputs, and seeded random cases. The same seed always yields the same corpus.

To confirm the harness detects real defects, the 32-bit addition was temporarily reintroduced in a scratch copy of the Java port. On a 141-case corpus the differential run reported 94 mismatches and exited non-zero.

## Recommended evolution

Keep Python as the reference, add any behavior change to the corpus first, and then update both implementations. If the Python side is retired, keep the generated corpus with expected outputs as a golden test set for Java.

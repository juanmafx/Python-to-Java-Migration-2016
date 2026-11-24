import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from tools.differential.corpus import generate_corpus
from tools.differential.runner import run_corpus
from tools.differential.store import persist

PROJECT_VERSION = "1.0.0"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare the Python and Java solvers on a seeded corpus.")
    parser.add_argument("--seed", type=int, default=20260101)
    parser.add_argument("--random-cases", type=int, default=200)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--database", type=Path)
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    corpus = generate_corpus(arguments.seed, arguments.random_cases)
    comparisons = run_corpus(corpus, arguments.workers)
    mismatched = [comparison for comparison in comparisons if not comparison.matched]
    summary = {
        "seed": arguments.seed,
        "cases": len(comparisons),
        "mismatches": len(mismatched),
        "categories": dict(sorted(Counter(case.category for case in corpus).items())),
        "mismatched_inputs_sha256": [comparison.input_sha256 for comparison in mismatched],
    }
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    if arguments.database:
        persist(arguments.database, PROJECT_VERSION, arguments.seed, comparisons)
    print(json.dumps({key: summary[key] for key in ("seed", "cases", "mismatches")}))
    return 1 if mismatched else 0


if __name__ == "__main__":
    sys.exit(main())

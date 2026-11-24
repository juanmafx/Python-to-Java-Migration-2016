import hashlib
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from tools.differential.corpus import Case

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PROCESS_TIMEOUT_SECONDS = 30


@dataclass(frozen=True)
class Outcome:
    stdout: bytes
    stderr: bytes
    exit_code: int


@dataclass(frozen=True)
class Comparison:
    index: int
    case: Case
    python: Outcome
    java: Outcome

    @property
    def matched(self) -> bool:
        expected = Outcome(self.case.expected_stdout, self.case.expected_stderr, self.case.expected_exit)
        return self.python == expected and self.java == expected

    @property
    def input_sha256(self) -> str:
        return hashlib.sha256(self.case.payload).hexdigest()


def python_command() -> list[str]:
    return [sys.executable, "-m", "integer_sum"]


def java_command() -> list[str]:
    classes = REPOSITORY_ROOT / "java" / "target" / "classes"
    return [
        "java",
        "-XX:TieredStopAtLevel=1",
        "-Xshare:auto",
        "-cp",
        str(classes),
        "io.github.juanmafx.integersum.cli.Application",
    ]


def execute(command: list[str], payload: bytes) -> Outcome:
    environment = {**os.environ, "PYTHONPATH": str(REPOSITORY_ROOT / "python" / "src")}
    completed = subprocess.run(
        command,
        input=payload,
        capture_output=True,
        timeout=PROCESS_TIMEOUT_SECONDS,
        env=environment,
        check=False,
    )
    return Outcome(completed.stdout, completed.stderr, completed.returncode)


def compare(index: int, case: Case) -> Comparison:
    return Comparison(
        index,
        case,
        execute(python_command(), case.payload),
        execute(java_command(), case.payload),
    )


def run_corpus(corpus: list[Case], workers: int) -> list[Comparison]:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(compare, range(len(corpus)), corpus))

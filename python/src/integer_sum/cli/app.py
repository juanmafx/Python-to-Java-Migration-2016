import sys
from typing import BinaryIO

from integer_sum.core.errors import InvalidInputError
from integer_sum.core.parsing import MAX_INPUT_BYTES
from integer_sum.core.solver import solve

EXIT_SUCCESS = 0
EXIT_INVALID_INPUT = 2


def run(stdin: BinaryIO, stdout: BinaryIO, stderr: BinaryIO) -> int:
    data = stdin.read(MAX_INPUT_BYTES + 1)
    try:
        output = solve(data)
    except InvalidInputError as error:
        stderr.write(f"error: {error.code.value}\n".encode("ascii"))
        stderr.flush()
        return EXIT_INVALID_INPUT
    stdout.write(output.encode("ascii"))
    stdout.flush()
    return EXIT_SUCCESS


def main() -> None:
    sys.exit(run(sys.stdin.buffer, sys.stdout.buffer, sys.stderr.buffer))

import sys
from typing import BinaryIO

from integer_sum.core.errors import InvalidInputError
from integer_sum.core.parsing import MAX_INPUT_BYTES, MAX_OPERAND_DIGITS
from integer_sum.core.solver import solve

EXIT_SUCCESS = 0
EXIT_INVALID_INPUT = 2
EXIT_IO_FAILURE = 3
IO_FAILURE_CODE = "io_failure"
MAX_RENDERED_DIGITS = MAX_OPERAND_DIGITS + 1


def emit(stream: BinaryIO | None, payload: bytes) -> bool:
    if stream is None:
        return False
    try:
        remaining = memoryview(payload)
        while remaining:
            written = stream.write(remaining)
            if not written:
                return False
            remaining = remaining[written:]
        stream.flush()
    except OSError:
        return False
    return True


def fail(stderr: BinaryIO | None, code: str, exit_code: int) -> int:
    emit(stderr, f"error: {code}\n".encode("ascii"))
    return exit_code


def run(stdin: BinaryIO | None, stdout: BinaryIO | None, stderr: BinaryIO | None) -> int:
    if stdin is None:
        return fail(stderr, IO_FAILURE_CODE, EXIT_IO_FAILURE)
    try:
        data = stdin.read(MAX_INPUT_BYTES + 1)
    except OSError:
        return fail(stderr, IO_FAILURE_CODE, EXIT_IO_FAILURE)
    try:
        output = solve(data)
    except InvalidInputError as error:
        return fail(stderr, error.code.value, EXIT_INVALID_INPUT)
    if not emit(stdout, output.encode("ascii")):
        return fail(stderr, IO_FAILURE_CODE, EXIT_IO_FAILURE)
    return EXIT_SUCCESS


def open_descriptor(descriptor: int, mode: str, buffering: int) -> BinaryIO | None:
    try:
        return open(descriptor, mode, buffering=buffering, closefd=False)
    except OSError:
        return None


def main() -> None:
    sys.set_int_max_str_digits(MAX_RENDERED_DIGITS)
    stdin = open_descriptor(0, "rb", -1)
    stdout = open_descriptor(1, "wb", 0)
    stderr = open_descriptor(2, "wb", 0)
    sys.exit(run(stdin, stdout, stderr))

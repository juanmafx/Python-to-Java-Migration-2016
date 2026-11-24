import io
import os
import subprocess
import sys
from pathlib import Path

import pytest

from integer_sum.cli.app import EXIT_INVALID_INPUT, EXIT_IO_FAILURE, EXIT_SUCCESS, run
from integer_sum.core.parsing import MAX_INPUT_BYTES, MAX_OPERAND_DIGITS

SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"


class FailingStream(io.BytesIO):
    def read(self, *_):
        raise OSError("read failed")

    def write(self, _):
        raise OSError("write failed")


class OneByteWriter(io.BytesIO):
    def write(self, data):
        return super().write(bytes(data[:1]))


def launch(payload, stdout, **environment):
    return subprocess.run(
        [sys.executable, "-m", "integer_sum"],
        input=payload,
        stdout=stdout,
        stderr=subprocess.PIPE,
        env={**os.environ, "PYTHONPATH": str(SOURCE_ROOT), **environment},
        check=False,
    )


def execute(payload):
    stdout, stderr = io.BytesIO(), io.BytesIO()
    return run(io.BytesIO(payload), stdout, stderr), stdout.getvalue(), stderr.getvalue()


def test_prints_sum_with_exact_format():
    assert execute(b"10\n9\n") == (EXIT_SUCCESS, b"X = 19\n", b"")


def test_handles_values_beyond_thirty_two_bits():
    assert execute(b"2147483647\n1\n") == (EXIT_SUCCESS, b"X = 2147483648\n", b"")


def test_reports_invalid_input_without_echoing_it():
    assert execute(b"secret-value 1") == (EXIT_INVALID_INPUT, b"", b"error: invalid_operand\n")


def test_bounds_the_bytes_it_reads():
    source = io.BytesIO(b"\0" * (MAX_INPUT_BYTES * 4))
    run(source, io.BytesIO(), io.BytesIO())
    assert source.tell() == MAX_INPUT_BYTES + 1


def test_reports_read_failure_without_traceback():
    stdout, stderr = io.BytesIO(), io.BytesIO()
    assert run(FailingStream(), stdout, stderr) == EXIT_IO_FAILURE
    assert (stdout.getvalue(), stderr.getvalue()) == (b"", b"error: io_failure\n")


def test_reports_write_failure_instead_of_succeeding():
    stderr = io.BytesIO()
    assert run(io.BytesIO(b"1 2"), FailingStream(), stderr) == EXIT_IO_FAILURE
    assert stderr.getvalue() == b"error: io_failure\n"


def test_reports_missing_streams():
    stderr = io.BytesIO()
    assert run(None, io.BytesIO(), stderr) == EXIT_IO_FAILURE
    assert run(io.BytesIO(b"1 2"), None, stderr) == EXIT_IO_FAILURE
    assert run(None, None, None) == EXIT_IO_FAILURE


def test_completes_partial_writes():
    stdout = OneByteWriter()
    assert run(io.BytesIO(b"10 9"), stdout, io.BytesIO()) == EXIT_SUCCESS
    assert stdout.getvalue() == b"X = 19\n"


def test_widest_sum_ignores_lower_interpreter_digit_limit():
    widest = b"9" * MAX_OPERAND_DIGITS
    completed = launch(widest + b" " + widest, subprocess.PIPE, PYTHONINTMAXSTRDIGITS="640")
    assert completed.returncode == EXIT_SUCCESS
    assert completed.stdout == f"X = {2 * (10**MAX_OPERAND_DIGITS - 1)}\n".encode("ascii")
    assert completed.stderr == b""


@pytest.mark.skipif(not Path("/dev/full").exists(), reason="requires /dev/full")
def test_full_device_is_reported_without_traceback():
    with open("/dev/full", "wb") as full_device:
        completed = launch(b"1 2", full_device)
    assert completed.returncode == EXIT_IO_FAILURE
    assert completed.stderr == b"error: io_failure\n"

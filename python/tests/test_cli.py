import io

from integer_sum.cli.app import EXIT_INVALID_INPUT, EXIT_SUCCESS, run
from integer_sum.core.parsing import MAX_INPUT_BYTES


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

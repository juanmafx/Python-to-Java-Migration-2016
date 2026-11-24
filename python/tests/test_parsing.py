import pytest

from integer_sum.core.errors import InputErrorCode, InvalidInputError
from integer_sum.core.parsing import MAX_INPUT_BYTES, MAX_OPERAND_DIGITS, parse_operands


@pytest.mark.parametrize("data", [b"10\n9\n", b"10 9", b"\t10\r\n9  ", b"+10 009"])
def test_accepts_supported_separators_and_signs(data):
    assert parse_operands(data) == (10, 9)


@pytest.mark.parametrize("data", [b"", b"   ", b"1", b"1 2 3"])
def test_rejects_wrong_operand_count(data):
    with pytest.raises(InvalidInputError) as caught:
        parse_operands(data)
    assert caught.value.code is InputErrorCode.WRONG_OPERAND_COUNT


@pytest.mark.parametrize(
    "data",
    [b"a 1", b"1_0 2", b"1.5 2", b"+ 2", b"- 2", b"--1 2", b"0x10 2", "\u0663 2".encode(), b"1\x0b2 3"],
)
def test_rejects_malformed_operands(data):
    with pytest.raises(InvalidInputError) as caught:
        parse_operands(data)
    assert caught.value.code is InputErrorCode.INVALID_OPERAND


def test_accepts_operand_at_digit_limit():
    digits = b"9" * MAX_OPERAND_DIGITS
    assert parse_operands(digits + b" 0")[0] == int(digits)


def test_rejects_operand_over_digit_limit():
    with pytest.raises(InvalidInputError) as caught:
        parse_operands(b"9" * (MAX_OPERAND_DIGITS + 1) + b" 0")
    assert caught.value.code is InputErrorCode.OPERAND_TOO_LONG


def test_rejects_oversized_input():
    with pytest.raises(InvalidInputError) as caught:
        parse_operands(b"\0" * (MAX_INPUT_BYTES + 1))
    assert caught.value.code is InputErrorCode.INPUT_TOO_LARGE

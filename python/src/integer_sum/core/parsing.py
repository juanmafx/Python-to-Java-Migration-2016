import re

from integer_sum.core.errors import InputErrorCode, InvalidInputError

MAX_INPUT_BYTES = 16_384
MAX_OPERAND_DIGITS = 4_096

_TOKEN = re.compile(rb"[^ \t\r\n]+")
_OPERAND = re.compile(rb"[+-]?[0-9]+")


def parse_operand(token: bytes) -> int:
    if _OPERAND.fullmatch(token) is None:
        raise InvalidInputError(InputErrorCode.INVALID_OPERAND)
    if len(token.lstrip(b"+-")) > MAX_OPERAND_DIGITS:
        raise InvalidInputError(InputErrorCode.OPERAND_TOO_LONG)
    return int(token)


def parse_operands(data: bytes) -> tuple[int, int]:
    if len(data) > MAX_INPUT_BYTES:
        raise InvalidInputError(InputErrorCode.INPUT_TOO_LARGE)
    tokens = _TOKEN.findall(data)
    if len(tokens) != 2:
        raise InvalidInputError(InputErrorCode.WRONG_OPERAND_COUNT)
    return parse_operand(tokens[0]), parse_operand(tokens[1])

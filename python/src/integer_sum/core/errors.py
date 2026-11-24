from enum import StrEnum


class InputErrorCode(StrEnum):
    INPUT_TOO_LARGE = "input_too_large"
    WRONG_OPERAND_COUNT = "wrong_operand_count"
    INVALID_OPERAND = "invalid_operand"
    OPERAND_TOO_LONG = "operand_too_long"


class InvalidInputError(ValueError):
    def __init__(self, code: InputErrorCode) -> None:
        super().__init__(code.value)
        self.code = code

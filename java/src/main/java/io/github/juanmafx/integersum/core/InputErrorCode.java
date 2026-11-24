package io.github.juanmafx.integersum.core;

public enum InputErrorCode {
    INPUT_TOO_LARGE("input_too_large"),
    WRONG_OPERAND_COUNT("wrong_operand_count"),
    INVALID_OPERAND("invalid_operand"),
    OPERAND_TOO_LONG("operand_too_long");

    private final String wireName;

    InputErrorCode(String wireName) {
        this.wireName = wireName;
    }

    public String wireName() {
        return wireName;
    }
}

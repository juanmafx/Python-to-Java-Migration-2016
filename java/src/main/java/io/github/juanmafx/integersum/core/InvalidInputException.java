package io.github.juanmafx.integersum.core;

public final class InvalidInputException extends RuntimeException {
    private static final long serialVersionUID = 1L;

    private final InputErrorCode code;

    public InvalidInputException(InputErrorCode code) {
        super(code.wireName());
        this.code = code;
    }

    public InputErrorCode code() {
        return code;
    }
}

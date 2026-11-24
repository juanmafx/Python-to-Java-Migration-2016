package io.github.juanmafx.integersum.core;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class OperandParser {
    public static final int MAX_INPUT_BYTES = 16_384;
    public static final int MAX_OPERAND_DIGITS = 4_096;

    private OperandParser() {
    }

    public static Operands parseOperands(byte[] data) {
        if (data.length > MAX_INPUT_BYTES) {
            throw new InvalidInputException(InputErrorCode.INPUT_TOO_LARGE);
        }
        List<byte[]> tokens = tokenize(data);
        if (tokens.size() != 2) {
            throw new InvalidInputException(InputErrorCode.WRONG_OPERAND_COUNT);
        }
        return new Operands(parseOperand(tokens.get(0)), parseOperand(tokens.get(1)));
    }

    public static BigInteger parseOperand(byte[] token) {
        int start = token.length > 0 && (token[0] == '+' || token[0] == '-') ? 1 : 0;
        if (start == token.length) {
            throw new InvalidInputException(InputErrorCode.INVALID_OPERAND);
        }
        for (int index = start; index < token.length; index++) {
            if (token[index] < '0' || token[index] > '9') {
                throw new InvalidInputException(InputErrorCode.INVALID_OPERAND);
            }
        }
        if (token.length - start > MAX_OPERAND_DIGITS) {
            throw new InvalidInputException(InputErrorCode.OPERAND_TOO_LONG);
        }
        return new BigInteger(new String(token, StandardCharsets.US_ASCII));
    }

    private static List<byte[]> tokenize(byte[] data) {
        List<byte[]> tokens = new ArrayList<>();
        int index = 0;
        while (index < data.length) {
            while (index < data.length && isSeparator(data[index])) {
                index++;
            }
            int start = index;
            while (index < data.length && !isSeparator(data[index])) {
                index++;
            }
            if (index > start) {
                tokens.add(Arrays.copyOfRange(data, start, index));
            }
        }
        return tokens;
    }

    private static boolean isSeparator(byte value) {
        return value == ' ' || value == '\t' || value == '\r' || value == '\n';
    }
}

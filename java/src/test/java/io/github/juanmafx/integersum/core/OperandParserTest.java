package io.github.juanmafx.integersum.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class OperandParserTest {
    private static byte[] ascii(String text) {
        return text.getBytes(StandardCharsets.UTF_8);
    }

    private static InputErrorCode failure(byte[] data) {
        return assertThrows(InvalidInputException.class, () -> OperandParser.parseOperands(data)).code();
    }

    @ParameterizedTest
    @ValueSource(strings = {"10\n9\n", "10 9", "\t10\r\n9  ", "+10 009"})
    void acceptsEverySupportedSeparatorAndSign(String input) {
        Operands operands = OperandParser.parseOperands(ascii(input));
        assertEquals(BigInteger.TEN, operands.left());
        assertEquals(BigInteger.valueOf(9), operands.right());
    }

    @ParameterizedTest
    @ValueSource(strings = {"", "   ", "1", "1 2 3"})
    void rejectsWrongOperandCount(String input) {
        assertEquals(InputErrorCode.WRONG_OPERAND_COUNT, failure(ascii(input)));
    }

    @ParameterizedTest
    @ValueSource(strings = {"a 1", "1_0 2", "1.5 2", "+ 2", "- 2", "--1 2", "0x10 2", "\u0663 2", "1\u000b2 3"})
    void rejectsMalformedOperands(String input) {
        assertEquals(InputErrorCode.INVALID_OPERAND, failure(ascii(input)));
    }

    @Test
    void acceptsOperandAtDigitLimit() {
        String digits = "9".repeat(OperandParser.MAX_OPERAND_DIGITS);
        assertEquals(new BigInteger(digits), OperandParser.parseOperands(ascii(digits + " 0")).left());
    }

    @Test
    void rejectsOperandOverDigitLimit() {
        String digits = "9".repeat(OperandParser.MAX_OPERAND_DIGITS + 1);
        assertEquals(InputErrorCode.OPERAND_TOO_LONG, failure(ascii(digits + " 0")));
    }

    @Test
    void rejectsOversizedInputBeforeTokenizing() {
        assertEquals(InputErrorCode.INPUT_TOO_LARGE, failure(new byte[OperandParser.MAX_INPUT_BYTES + 1]));
    }
}

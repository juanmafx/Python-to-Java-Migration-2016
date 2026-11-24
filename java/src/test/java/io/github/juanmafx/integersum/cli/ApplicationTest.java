package io.github.juanmafx.integersum.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;

import io.github.juanmafx.integersum.core.OperandParser;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

class ApplicationTest {
    private final ByteArrayOutputStream stdout = new ByteArrayOutputStream();
    private final ByteArrayOutputStream stderr = new ByteArrayOutputStream();

    private int execute(byte[] input) throws IOException {
        return Application.run(new ByteArrayInputStream(input), stdout, stderr);
    }

    @Test
    void printsTheSumWithExactFormat() throws IOException {
        assertEquals(Application.EXIT_SUCCESS, execute("10\n9\n".getBytes(StandardCharsets.US_ASCII)));
        assertEquals("X = 19\n", stdout.toString(StandardCharsets.US_ASCII));
        assertEquals(0, stderr.size());
    }

    @Test
    void doesNotOverflowAtThirtyTwoBitBoundary() throws IOException {
        execute("2147483647\n1\n".getBytes(StandardCharsets.US_ASCII));
        assertEquals("X = 2147483648\n", stdout.toString(StandardCharsets.US_ASCII));
    }

    @Test
    void reportsInvalidInputWithoutEchoingIt() throws IOException {
        assertEquals(Application.EXIT_INVALID_INPUT, execute("secret-value 1".getBytes(StandardCharsets.US_ASCII)));
        assertEquals("error: invalid_operand\n", stderr.toString(StandardCharsets.US_ASCII));
        assertEquals(0, stdout.size());
    }

    @Test
    void boundsTheBytesItReads() throws IOException {
        assertEquals(Application.EXIT_INVALID_INPUT, execute(new byte[OperandParser.MAX_INPUT_BYTES * 4]));
        assertEquals("error: input_too_large\n", stderr.toString(StandardCharsets.US_ASCII));
    }
}

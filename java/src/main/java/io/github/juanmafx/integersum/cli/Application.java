package io.github.juanmafx.integersum.cli;

import io.github.juanmafx.integersum.core.InvalidInputException;
import io.github.juanmafx.integersum.core.OperandParser;
import io.github.juanmafx.integersum.core.Solver;
import java.io.FileDescriptor;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public final class Application {
    static final int EXIT_SUCCESS = 0;
    static final int EXIT_INVALID_INPUT = 2;
    static final int EXIT_IO_FAILURE = 3;
    private static final String IO_FAILURE_CODE = "io_failure";

    private Application() {
    }

    public static int run(InputStream stdin, OutputStream stdout, OutputStream stderr) {
        byte[] data;
        try {
            data = stdin.readNBytes(OperandParser.MAX_INPUT_BYTES + 1);
        } catch (IOException error) {
            return fail(stderr, IO_FAILURE_CODE, EXIT_IO_FAILURE);
        }
        String output;
        try {
            output = Solver.solve(data);
        } catch (InvalidInputException error) {
            return fail(stderr, error.code().wireName(), EXIT_INVALID_INPUT);
        }
        try {
            stdout.write(output.getBytes(StandardCharsets.US_ASCII));
            stdout.flush();
        } catch (IOException error) {
            return fail(stderr, IO_FAILURE_CODE, EXIT_IO_FAILURE);
        }
        return EXIT_SUCCESS;
    }

    private static int fail(OutputStream stderr, String code, int exitCode) {
        try {
            stderr.write(("error: " + code + "\n").getBytes(StandardCharsets.US_ASCII));
            stderr.flush();
        } catch (IOException error) {
            return exitCode;
        }
        return exitCode;
    }

    public static void main(String[] args) {
        System.exit(run(
                System.in,
                new FileOutputStream(FileDescriptor.out),
                new FileOutputStream(FileDescriptor.err)));
    }
}

package io.github.juanmafx.integersum.cli;

import io.github.juanmafx.integersum.core.InvalidInputException;
import io.github.juanmafx.integersum.core.OperandParser;
import io.github.juanmafx.integersum.core.Solver;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public final class Application {
    static final int EXIT_SUCCESS = 0;
    static final int EXIT_INVALID_INPUT = 2;

    private Application() {
    }

    public static int run(InputStream stdin, OutputStream stdout, OutputStream stderr) throws IOException {
        byte[] data = stdin.readNBytes(OperandParser.MAX_INPUT_BYTES + 1);
        String output;
        try {
            output = Solver.solve(data);
        } catch (InvalidInputException error) {
            stderr.write(("error: " + error.code().wireName() + "\n").getBytes(StandardCharsets.US_ASCII));
            stderr.flush();
            return EXIT_INVALID_INPUT;
        }
        stdout.write(output.getBytes(StandardCharsets.US_ASCII));
        stdout.flush();
        return EXIT_SUCCESS;
    }

    public static void main(String[] args) throws IOException {
        System.exit(run(System.in, System.out, System.err));
    }
}

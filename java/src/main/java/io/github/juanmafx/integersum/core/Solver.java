package io.github.juanmafx.integersum.core;

import java.math.BigInteger;

public final class Solver {
    private Solver() {
    }

    public static BigInteger add(BigInteger left, BigInteger right) {
        return left.add(right);
    }

    public static String render(BigInteger total) {
        return "X = " + total + "\n";
    }

    public static String solve(byte[] data) {
        Operands operands = OperandParser.parseOperands(data);
        return render(add(operands.left(), operands.right()));
    }
}

package io.github.juanmafx.integersum.core;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import net.jqwik.api.Arbitraries;
import net.jqwik.api.Arbitrary;
import net.jqwik.api.ForAll;
import net.jqwik.api.Property;
import net.jqwik.api.Provide;

class SolverProperties {
    private static final String SEED = "20260101";

    @Provide
    Arbitrary<BigInteger> wideIntegers() {
        BigInteger bound = BigInteger.TEN.pow(200);
        return Arbitraries.bigIntegers().between(bound.negate(), bound);
    }

    @Property(seed = SEED)
    void additionIsCommutative(@ForAll("wideIntegers") BigInteger left, @ForAll("wideIntegers") BigInteger right) {
        assertEquals(Solver.add(left, right), Solver.add(right, left));
    }

    @Property(seed = SEED)
    void additionIsAssociative(
            @ForAll("wideIntegers") BigInteger first,
            @ForAll("wideIntegers") BigInteger second,
            @ForAll("wideIntegers") BigInteger third) {
        assertEquals(
                Solver.add(Solver.add(first, second), third),
                Solver.add(first, Solver.add(second, third)));
    }

    @Property(seed = SEED)
    void zeroIsTheIdentity(@ForAll("wideIntegers") BigInteger value) {
        assertEquals(value, Solver.add(value, BigInteger.ZERO));
    }

    @Property(seed = SEED)
    void solveRoundTripsThroughDecimalText(
            @ForAll("wideIntegers") BigInteger left, @ForAll("wideIntegers") BigInteger right) {
        byte[] input = (left + "\n" + right + "\n").getBytes(StandardCharsets.US_ASCII);
        assertEquals("X = " + left.add(right) + "\n", Solver.solve(input));
    }

    @Property(seed = SEED)
    void arbitraryBytesEitherSolveOrFailWithTypedError(@ForAll byte[] data) {
        try {
            assertEquals('X', Solver.solve(data).charAt(0));
        } catch (InvalidInputException error) {
            assertEquals(error.code().wireName(), error.getMessage());
        }
    }
}

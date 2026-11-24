import random
from dataclasses import dataclass

MAX_INPUT_BYTES = 16_384
MAX_OPERAND_DIGITS = 4_096
RANDOM_DIGIT_CEILING = 64
CATEGORIES = ("boundary", "random", "formatting", "invalid")


@dataclass(frozen=True)
class Case:
    category: str
    payload: bytes
    expected_stdout: bytes
    expected_stderr: bytes
    expected_exit: int


def valid_case(category: str, left: int, right: int, payload: bytes) -> Case:
    return Case(category, payload, f"X = {left + right}\n".encode("ascii"), b"", 0)


def invalid_case(payload: bytes, code: str) -> Case:
    return Case("invalid", payload, b"", f"error: {code}\n".encode("ascii"), 2)


def random_decimal(rng: random.Random, ceiling: int = RANDOM_DIGIT_CEILING) -> str:
    length = rng.randint(1, ceiling)
    first = rng.choice("123456789")
    rest = "".join(rng.choices("0123456789", k=length - 1))
    sign = rng.choice(("", "-"))
    return f"{sign}{first}{rest}"


def boundary_cases() -> list[Case]:
    limits = [0, 1, -1, 2**31 - 1, -(2**31), 2**31, 2**63 - 1, -(2**63), 2**63, 10**18]
    cases = [
        valid_case("boundary", left, right, f"{left}\n{right}\n".encode("ascii"))
        for left in limits
        for right in limits
    ]
    widest = "9" * MAX_OPERAND_DIGITS
    cases.append(valid_case("boundary", int(widest), int(widest), f"{widest}\n{widest}\n".encode("ascii")))
    cases.append(valid_case("boundary", -int(widest), int(widest), f"-{widest} {widest}".encode("ascii")))
    return cases


def invalid_cases() -> list[Case]:
    over_limit = b"1" * (MAX_OPERAND_DIGITS + 1)
    return [
        invalid_case(b"", "wrong_operand_count"),
        invalid_case(b" \n\t", "wrong_operand_count"),
        invalid_case(b"1\n", "wrong_operand_count"),
        invalid_case(b"1 2 3", "wrong_operand_count"),
        invalid_case(b"a b", "invalid_operand"),
        invalid_case(b"1_0 2", "invalid_operand"),
        invalid_case(b"1.5 2", "invalid_operand"),
        invalid_case(b"0x10 2", "invalid_operand"),
        invalid_case(b"+ 2", "invalid_operand"),
        invalid_case(b"-- 2", "invalid_operand"),
        invalid_case(b"1e3 2", "invalid_operand"),
        invalid_case("\u0663 2".encode("utf-8"), "invalid_operand"),
        invalid_case(b"\xef\xbb\xbf1 2", "invalid_operand"),
        invalid_case(b"1\x0b2 3", "invalid_operand"),
        invalid_case(b"1\x00 2", "invalid_operand"),
        invalid_case(over_limit + b" 1", "operand_too_long"),
        invalid_case(b"1 " + over_limit, "operand_too_long"),
        invalid_case(b"1" * (MAX_INPUT_BYTES + 1), "input_too_large"),
        invalid_case(b" " * (MAX_INPUT_BYTES * 2), "input_too_large"),
    ]


def formatted_case(rng: random.Random) -> Case:
    left, right = random_decimal(rng), random_decimal(rng)
    separator = rng.choice((" ", "\n", "\r\n", "\t", "  \n\t"))
    lead = rng.choice(("", " ", "\n", "\t"))
    trail = rng.choice(("", "\n", "\r\n", "  "))
    zeros = "0" * rng.randint(0, 5)
    left_text = f"-{zeros}{left[1:]}" if left.startswith("-") else f"+{zeros}{left}"
    payload = f"{lead}{left_text}{separator}{right}{trail}".encode("ascii")
    return valid_case("formatting", int(left), int(right), payload)


def random_case(rng: random.Random) -> Case:
    left, right = random_decimal(rng), random_decimal(rng)
    return valid_case("random", int(left), int(right), f"{left}\n{right}\n".encode("ascii"))


def generate_corpus(seed: int, random_count: int) -> list[Case]:
    rng = random.Random(seed)
    generated = [
        formatted_case(rng) if index % 2 else random_case(rng)
        for index in range(random_count)
    ]
    return boundary_cases() + invalid_cases() + generated

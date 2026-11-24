from integer_sum.core.parsing import parse_operands


def add(left: int, right: int) -> int:
    return left + right


def render(total: int) -> str:
    return f"X = {total}\n"


def solve(data: bytes) -> str:
    left, right = parse_operands(data)
    return render(add(left, right))

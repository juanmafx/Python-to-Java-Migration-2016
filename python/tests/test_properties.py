from hypothesis import given
from hypothesis import strategies as st

from integer_sum.core.errors import InvalidInputError
from integer_sum.core.solver import add, render, solve

BOUND = 10**200
wide_integers = st.integers(min_value=-BOUND, max_value=BOUND)
separators = st.text(alphabet=" \t\r\n", min_size=1, max_size=4)


@given(wide_integers, wide_integers)
def test_addition_is_commutative(left, right):
    assert add(left, right) == add(right, left)


@given(wide_integers, wide_integers, wide_integers)
def test_addition_is_associative(first, second, third):
    assert add(add(first, second), third) == add(first, add(second, third))


@given(wide_integers)
def test_zero_is_the_identity(value):
    assert add(value, 0) == value


@given(wide_integers, wide_integers, separators)
def test_solve_round_trips_through_decimal_text(left, right, separator):
    payload = f"{left}{separator}{right}\n".encode("ascii")
    assert solve(payload) == render(left + right)


@given(st.binary(max_size=64))
def test_arbitrary_bytes_solve_or_fail_with_typed_error(data):
    try:
        assert solve(data).startswith("X = ")
    except InvalidInputError as error:
        assert str(error) == error.code.value

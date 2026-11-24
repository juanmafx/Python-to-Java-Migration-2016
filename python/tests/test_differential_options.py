import pytest

from tools.differential.__main__ import SIGNED_64_BIT_MAX, SIGNED_64_BIT_MIN, parse_arguments


@pytest.mark.parametrize(
    "arguments",
    [
        ["--workers", "0"],
        ["--workers", "-1"],
        ["--workers", "x"],
        ["--random-cases", "-1"],
        ["--seed", str(SIGNED_64_BIT_MAX + 1)],
        ["--seed", str(SIGNED_64_BIT_MIN - 1)],
        ["--seed", "9" * 5000],
    ],
)
def test_rejects_out_of_range_options(arguments, capsys):
    with pytest.raises(SystemExit) as caught:
        parse_arguments(arguments)
    assert caught.value.code == 2
    assert "Traceback" not in capsys.readouterr().err


def test_accepts_range_limits():
    parsed = parse_arguments(["--seed", str(SIGNED_64_BIT_MIN), "--random-cases", "0", "--workers", "1"])
    assert (parsed.seed, parsed.random_cases, parsed.workers) == (SIGNED_64_BIT_MIN, 0, 1)
    assert parse_arguments(["--seed", str(SIGNED_64_BIT_MAX)]).seed == SIGNED_64_BIT_MAX

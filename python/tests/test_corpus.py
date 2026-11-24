import random
import re
from pathlib import Path

from tools.differential.corpus import (
    CATEGORIES,
    RANDOM_DIGIT_CEILING,
    generate_corpus,
    random_decimal,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CHI_SQUARE_CRITICAL_DF63_ALPHA_0001 = 103.5


def test_corpus_is_reproducible_for_a_seed():
    assert generate_corpus(7, 50) == generate_corpus(7, 50)


def test_corpus_changes_with_the_seed():
    assert generate_corpus(7, 50) != generate_corpus(8, 50)


def test_corpus_covers_every_category():
    assert {case.category for case in generate_corpus(7, 10)} == set(CATEGORIES)


def test_random_digit_lengths_are_uniform():
    rng = random.Random(20260101)
    samples_per_bin = 100
    observed = [0] * RANDOM_DIGIT_CEILING
    for _ in range(samples_per_bin * RANDOM_DIGIT_CEILING):
        observed[len(random_decimal(rng).lstrip("-")) - 1] += 1
    statistic = sum((count - samples_per_bin) ** 2 / samples_per_bin for count in observed)
    assert statistic < CHI_SQUARE_CRITICAL_DF63_ALPHA_0001


def test_versions_are_consistent():
    from integer_sum import __version__
    from tools.differential.__main__ import PROJECT_VERSION

    pom = (REPOSITORY_ROOT / "java" / "pom.xml").read_text(encoding="utf-8")
    pyproject = (REPOSITORY_ROOT / "python" / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r"<artifactId>integer-sum</artifactId>\s*<version>([^<]+)", pom).group(1) == __version__
    assert re.search(r'^version = "([^"]+)"', pyproject, re.MULTILINE).group(1) == __version__
    assert PROJECT_VERSION == __version__

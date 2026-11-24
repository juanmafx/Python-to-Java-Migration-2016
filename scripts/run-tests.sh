#!/usr/bin/env bash
# Runs every suite and writes reports/tests/ from the actual results.
set -uo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
python_bin="${PYTHON:-python3}"
[[ "$python_bin" == */* && "$python_bin" != /* ]] && python_bin="$PWD/$python_bin"
maven_bin="${MAVEN:-mvn}"
status=0
rm -rf build
mkdir -p build

(cd python && "$python_bin" -m pytest --junitxml=../build/pytest.xml -o junit_family=xunit2) || status=1
"$maven_bin" -q -B -f java/pom.xml clean verify || status=1

if [[ -d java/target/classes ]]; then
    PYTHONPATH=python/src "$python_bin" -m tools.differential --output build/differential.json || status=1
else
    status=1
fi

if [[ -f build/pytest.xml && -f build/differential.json ]]; then
    "$python_bin" tools/reporting/build_report.py build reports/tests || status=1
else
    status=1
fi

exit "$status"

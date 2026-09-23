@pytest.mark.skipif(NO_MYPY, reason="Mypy is not installed")
@pytest.mark.parametrize("path", get_test_cases(FAIL_DIR))
def test_fail(path):
    __tracebackhide__ = True

    with open(path) as fin:
        lines = fin.readlines()

    errors = defaultdict(lambda: "")

    output_mypy = OUTPUT_MYPY
    assert path in output_mypy
    for error_line in output_mypy[path]:
        error_line = _strip_filename(error_line)
        match = re.match(
            r"(?P<lineno>\d+): (error|note): .+$",
            error_line,
        )
        if match is None:
            raise ValueError(f"Unexpected error line format: {error_line}")
        lineno = int(match.group('lineno'))
        errors[lineno] += f'{error_line}\n'

    for i, line in enumerate(lines):
        lineno = i + 1
        if line.startswith('#') or (" E:" not in line and lineno not in errors):
            continue

        target_line = lines[lineno - 1]
        if "# E:" in target_line:
            marker = target_line.split("# E:")[-1].strip()
            expected_error = errors.get(lineno)
            _test_fail(path, marker, expected_error, lineno)
        else:
            pytest.fail(f"Unexpected mypy output\n\n{errors[lineno]}")

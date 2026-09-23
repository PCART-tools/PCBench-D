@pytest.mark.skipif(NO_MYPY, reason="Mypy is not installed")
@pytest.mark.parametrize("path", get_test_cases(REVEAL_DIR))
def test_reveal(path):
    __tracebackhide__ = True

    with open(path) as fin:
        lines = _parse_reveals(fin)

    output_mypy = OUTPUT_MYPY
    assert path in output_mypy
    for error_line in output_mypy[path]:
        match = re.match(
            r"^.+\.py:(?P<lineno>\d+): note: .+$",
            error_line,
        )
        if match is None:
            raise ValueError(f"Unexpected reveal line format: {error_line}")
        lineno = int(match.group("lineno")) - 1
        assert "Revealed type is" in error_line

        marker = lines[lineno]
        _test_reveal(path, marker, error_line, 1 + lineno)

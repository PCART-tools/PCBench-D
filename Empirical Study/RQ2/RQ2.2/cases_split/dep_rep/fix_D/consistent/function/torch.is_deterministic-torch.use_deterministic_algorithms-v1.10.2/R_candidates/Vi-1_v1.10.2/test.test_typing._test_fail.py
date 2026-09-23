def _test_fail(path: str, error: str, expected_error: Optional[str], lineno: int) -> None:
    if expected_error is None:
        raise AssertionError(_FAIL_MSG1.format(lineno, error))
    elif error not in expected_error:
        raise AssertionError(_FAIL_MSG2.format(lineno, expected_error, error))

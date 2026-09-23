def discover_tests(
        base_dir: Optional[pathlib.Path] = None,
        blocklisted_patterns: Optional[List[str]] = None,
        blocklisted_tests: Optional[List[str]] = None,
        extra_tests: Optional[List[str]] = None) -> List[str]:
    """
    Searches for all python files starting with test_ excluding one specified by patterns
    """
    def skip_test_p(name: str) -> bool:
        rc = False
        if blocklisted_patterns is not None:
            rc |= any(name.startswith(pattern) for pattern in blocklisted_patterns)
        if blocklisted_tests is not None:
            rc |= name in blocklisted_tests
        return rc
    cwd = pathlib.Path(__file__).resolve().parent if base_dir is None else base_dir
    all_py_files = list(cwd.glob('**/test_*.py'))
    rc = [str(fname.relative_to(cwd))[:-3] for fname in all_py_files]
    # Invert slashes on Windows
    if sys.platform == "win32":
        rc = [name.replace('\\', '/') for name in rc]
    rc = [test for test in rc if not skip_test_p(test)]
    if extra_tests is not None:
        rc += extra_tests
    return sorted(rc)

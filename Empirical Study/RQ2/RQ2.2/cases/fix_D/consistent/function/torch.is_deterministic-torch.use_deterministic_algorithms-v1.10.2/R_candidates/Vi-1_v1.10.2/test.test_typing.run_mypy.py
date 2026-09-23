@pytest.mark.skipif(NO_MYPY, reason="Mypy is not installed")
@pytest.fixture(scope="module", autouse=True)
def run_mypy() -> None:
    """Clears the cache and run mypy before running any of the typing tests.

    The mypy results are cached in `OUTPUT_MYPY` for further use.

    """
    if os.path.isdir(CACHE_DIR):
        shutil.rmtree(CACHE_DIR)

    for directory in (REVEAL_DIR, PASS_DIR, FAIL_DIR):
        # Run mypy
        stdout, stderr, _ = api.run(
            [
                "--show-absolute-path",
                "--config-file",
                MYPY_INI,
                "--cache-dir",
                CACHE_DIR,
                directory,
            ]
        )
        assert not stderr, directory
        stdout = stdout.replace("*", "")

        # Parse the output
        iterator = itertools.groupby(stdout.split("\n"), key=_key_func)
        OUTPUT_MYPY.update((k, list(v)) for k, v in iterator if k)

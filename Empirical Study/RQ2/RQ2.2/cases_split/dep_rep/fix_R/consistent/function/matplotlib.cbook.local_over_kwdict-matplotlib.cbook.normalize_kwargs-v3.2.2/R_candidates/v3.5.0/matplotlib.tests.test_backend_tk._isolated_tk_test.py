def _isolated_tk_test(success_count, func=None):
    """
    A decorator to run *func* in a subprocess and assert that it prints
    "success" *success_count* times and nothing on stderr.

    TkAgg tests seem to have interactions between tests, so isolate each test
    in a subprocess. See GH#18261

    The decorated function must be fully self-contained, and thus perform
    all the imports it needs.  Because its source is extracted and run by
    itself, coverage will consider it as not being run, so it should be marked
    with ``# pragma: no cover``
    """

    if func is None:
        return functools.partial(_isolated_tk_test, success_count)

    # Remove decorators.
    source = re.search(r"(?ms)^def .*", inspect.getsource(func)).group(0)

    @functools.wraps(func)
    def test_func():
        try:
            proc = subprocess.run(
                [sys.executable, "-c", f"{source}\n{func.__name__}()"],
                env={**os.environ, "MPLBACKEND": "TkAgg"},
                timeout=_test_timeout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                universal_newlines=True,
            )
        except subprocess.TimeoutExpired:
            pytest.fail("Subprocess timed out")
        except subprocess.CalledProcessError:
            pytest.fail("Subprocess failed to test intended behavior")
        else:
            # macOS may actually emit irrelevant errors about Accelerated
            # OpenGL vs. software OpenGL, so suppress them.
            # Asserting stderr first (and printing it on failure) should be
            # more helpful for debugging that printing a failed success count.
            assert not [line for line in proc.stderr.splitlines()
                        if "OpenGL" not in line]
            assert proc.stdout.count("success") == success_count

    return test_func

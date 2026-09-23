def noarchTest(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if TEST_SKIP_NOARCH:
            raise unittest.SkipTest("test is noarch: we are skipping noarch tests due to TEST_SKIP_NOARCH")
        else:
            fn(*args, **kwargs)
    return wrapper

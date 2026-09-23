def skipIfMPS(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if TEST_MPS:
            raise unittest.SkipTest("test doesn't currently work with MPS")
        else:
            fn(*args, **kwargs)
    return wrapper

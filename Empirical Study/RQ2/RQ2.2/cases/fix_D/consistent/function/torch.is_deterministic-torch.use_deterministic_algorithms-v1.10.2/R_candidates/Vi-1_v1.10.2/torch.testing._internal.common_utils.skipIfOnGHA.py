def skipIfOnGHA(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if ON_GHA:
            raise unittest.SkipTest("Test disabled for GHA")
        else:
            fn(*args, **kwargs)
    return wrapper

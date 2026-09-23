def skipIfTBB(message="This test makes TBB sad"):
    def dec_fn(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if IS_TBB:
                raise unittest.SkipTest(message)
            else:
                fn(*args, **kwargs)
        return wrapper
    return dec_fn

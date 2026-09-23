def skipIfMPSOnMacOS13(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if TEST_MPS and int(MACOS_VERSION) == 13:
            raise unittest.SkipTest("Test crashes MPSGraph on MacOS13")
        else:
            fn(*args, **kwargs)
    return wrapper

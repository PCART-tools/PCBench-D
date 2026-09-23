def xfail(func):
    try:
        func()
        raise Exception("XFailed test passed")  # pragma:nocover
    except Exception:
        pass

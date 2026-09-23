def xfail(func):
    try:
        func()
        raise Exception("XFailed test passed")  # pragma:nocover  # noqa: TRY002
    except Exception:
        pass

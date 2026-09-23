def skip_if_rocm(func):
    """Skips a test for ROCm"""
    func.skip_if_rocm = True

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not TEST_WITH_ROCM:
            return func(*args, **kwargs)
        sys.exit(TEST_SKIPS["skipIfRocm"].exit_code)

    return wrapper

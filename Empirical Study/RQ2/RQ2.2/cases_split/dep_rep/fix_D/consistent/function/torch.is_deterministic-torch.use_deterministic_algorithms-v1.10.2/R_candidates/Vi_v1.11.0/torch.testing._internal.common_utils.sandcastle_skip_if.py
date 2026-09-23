def sandcastle_skip_if(condition, reason):
    """
    Similar to unittest.skipIf, however in the sandcastle environment it just
    "passes" the test instead to avoid creating tasks complaining about tests
    skipping continuously.
    """
    def decorator(func):

        if not IS_SANDCASTLE and condition:
            func.__unittest_skip__ = True
            func.__unittest_skip_why__ = reason
            return func

        @wraps(func)
        def wrapper(*args, **kwargs):
            if condition and IS_SANDCASTLE:
                print(f'Skipping {func.__name__} on sandcastle for following reason: {reason}', file=sys.stderr)
                return
            else:
                return func(*args, **kwargs)
        return wrapper

    return decorator

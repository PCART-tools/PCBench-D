def _safety_decorator(safety_marker, func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        return safety_marker(func(*args, **kwargs))
    return wrapped

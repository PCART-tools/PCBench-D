def triggered_wrapper(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        wrapped._triggered = True
        return f(*args, **kwargs)

    wrapped._triggered = False
    return wrapped

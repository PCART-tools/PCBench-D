def tokenize(*args, **kwargs):
    """Mapping function from task -> consistent name.

    Parameters
    ----------
    args : object
        Python objects that summarize the task.
    pure : boolean, optional
        If True, a consistent hash function is tried on the input. If this
        fails, then a unique identifier is used. If False (default), then a
        unique identifier is always used.
    """
    if kwargs.pop('pure', False):
        return base.tokenize(*args, **kwargs)
    else:
        return str(uuid.uuid4())

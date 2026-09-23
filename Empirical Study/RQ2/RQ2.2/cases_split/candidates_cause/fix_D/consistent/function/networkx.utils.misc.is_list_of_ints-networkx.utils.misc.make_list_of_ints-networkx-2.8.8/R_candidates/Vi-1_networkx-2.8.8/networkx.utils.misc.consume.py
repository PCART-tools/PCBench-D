def consume(iterator):
    """Consume the iterator entirely.

    .. deprecated:: 2.6
        This is deprecated and will be removed in NetworkX v3.0.
    """
    # Feed the entire iterator into a zero-length deque.
    msg = (
        "consume is deprecated and will be removed in version 3.0. "
        "Use ``collections.deque(iterator, maxlen=0)`` instead."
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)
    deque(iterator, maxlen=0)

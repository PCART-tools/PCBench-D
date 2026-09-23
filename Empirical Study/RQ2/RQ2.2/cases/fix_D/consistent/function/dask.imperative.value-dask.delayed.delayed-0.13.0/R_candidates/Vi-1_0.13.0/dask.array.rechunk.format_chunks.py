def format_chunks(chunks):
    """
    >>> format_chunks((10 * (3,), 3 * (10,)))
    (10*[3], 3*[10])
    """
    assert isinstance(chunks, tuple)
    return tuple(format_blocks(c) for c in chunks)

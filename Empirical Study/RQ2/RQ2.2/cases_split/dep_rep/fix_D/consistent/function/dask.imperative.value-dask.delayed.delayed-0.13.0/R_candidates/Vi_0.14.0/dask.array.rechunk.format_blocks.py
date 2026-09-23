def format_blocks(blocks):
    """
    Pretty-format *blocks*.

    >>> format_blocks((10, 10, 10))
    3*[10]
    >>> format_blocks((2, 3, 4))
    [2, 3, 4]
    >>> format_blocks((10, 10, 5, 6, 2, 2, 2, 7))
    2*[10] | [5, 6] | 3*[2] | [7]
    """
    assert (isinstance(blocks, tuple) and
            all(isinstance(x, int) for x in blocks))
    return _PrettyBlocks(blocks)

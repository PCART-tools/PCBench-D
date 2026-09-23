def _fix2comp(num):
    """Convert from two's complement to negative."""
    assert 0 <= num < 2**32
    if num & 2**31:
        return num - 2**32
    else:
        return num

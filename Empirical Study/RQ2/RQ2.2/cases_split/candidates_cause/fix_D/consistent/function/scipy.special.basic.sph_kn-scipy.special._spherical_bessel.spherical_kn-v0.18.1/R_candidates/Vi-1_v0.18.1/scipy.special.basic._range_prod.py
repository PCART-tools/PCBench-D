def _range_prod(lo, hi):
    """
    Product of a range of numbers.

    Returns the product of
    lo * (lo+1) * (lo+2) * ... * (hi-2) * (hi-1) * hi
    = hi! / (lo-1)!

    Breaks into smaller products first for speed:
    _range_prod(2, 9) = ((2*3)*(4*5))*((6*7)*(8*9))
    """
    if lo + 1 < hi:
        mid = (hi + lo) // 2
        return _range_prod(lo, mid) * _range_prod(mid + 1, hi)
    if lo == hi:
        return lo
    return lo * hi

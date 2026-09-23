def round_to(c, s):
    """ Return a chunk dimension that is close to an even multiple or factor

    We want values for c that are nicely aligned with s.

    If c is smaller than s then we want the largest factor of s that is less than the
    desired chunk size, but not less than half, which is too much.  If no such
    factor exists then we just go with the original chunk size and accept an
    uneven chunk at the end.

    If c is larger than s then we want the largest multiple of s that is still
    smaller than c.
    """
    if c <= s:
        try:
            return max(f for f in factors(s) if c / 2 <= f <= c)
        except ValueError:  # no matching factors within factor of two
            return max(1, int(c))
    else:
        return c // s * s

def edge(a, b, tie_breaker=hash):
    """ A should be checked before B
    Tie broken by tie_breaker, defaults to ``hash``
    """
    # A either supercedes B and B does not supercede A or if B does then call
    # tie_breaker
    return supercedes(a, b) and (not supercedes(b, a) or tie_breaker(a) > tie_breaker(b))

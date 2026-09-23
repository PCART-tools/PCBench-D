def _simplify(expr):
    """ Wrapper to avoid circular imports. """
    from sympy.simplify.simplify import simplify
    return simplify(expr)

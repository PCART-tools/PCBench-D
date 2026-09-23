def sympy_generic_le(lower, upper):
    if isinstance(lower, sympy.Expr):
        assert isinstance(upper, sympy.Expr)
        # instead of lower <= upper, we do upper >= lower since upper is mostly int_oo
        # and we have better code paths there.
        return upper >= lower
    else:
        # only negative condition is True > False
        assert isinstance(lower, SympyBoolean) and isinstance(upper, SympyBoolean), (
            lower,
            upper,
        )
        return not (lower and not upper)

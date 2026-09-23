def _getscaleoffset(expr):
    stub = ["stub"]
    data = expr(_E(stub)).data
    try:
        (a, b, c) = data  # simplified syntax
        if a is stub and b == "__mul__" and isinstance(c, numbers.Number):
            return c, 0.0
        if a is stub and b == "__add__" and isinstance(c, numbers.Number):
            return 1.0, c
    except TypeError:
        pass
    try:
        ((a, b, c), d, e) = data  # full syntax
        if (
            a is stub
            and b == "__mul__"
            and isinstance(c, numbers.Number)
            and d == "__add__"
            and isinstance(e, numbers.Number)
        ):
            return c, e
    except TypeError:
        pass
    raise ValueError("illegal expression")

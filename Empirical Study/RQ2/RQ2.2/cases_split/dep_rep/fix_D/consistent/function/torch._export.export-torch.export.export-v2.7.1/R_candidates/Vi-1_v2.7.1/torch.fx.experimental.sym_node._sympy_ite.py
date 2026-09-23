def _sympy_ite(a, t, f):
    import sympy

    return sympy.Piecewise((t, a), (f, True))

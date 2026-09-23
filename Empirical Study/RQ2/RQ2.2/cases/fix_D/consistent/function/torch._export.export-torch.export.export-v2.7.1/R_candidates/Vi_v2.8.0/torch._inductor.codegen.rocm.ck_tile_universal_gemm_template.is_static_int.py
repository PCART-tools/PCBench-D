def is_static_int(number):
    import sympy

    return isinstance(number, (int, sympy.Integer))

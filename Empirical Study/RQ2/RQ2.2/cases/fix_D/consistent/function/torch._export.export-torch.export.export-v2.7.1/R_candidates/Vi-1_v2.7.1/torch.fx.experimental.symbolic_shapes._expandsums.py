def _expandsums(args: list[sympy.Expr]) -> tuple[sympy.Expr, bool]:
    adds, other = [], []
    for arg in args:
        if arg.is_Add:
            adds.append(arg)
        else:
            other.append(arg)

    result = [sympy.Mul(*other)]
    for add in adds:
        result = [a * b for a, b in itertools.product(result, add.args)]

    result = sympy.Add(*result)
    return result, len(adds) > 1 or (len(adds) > 0 and len(other) > 0)

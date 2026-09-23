def broadcast_symbolic_shapes(a, b):
    """
    Broadcasting logic based on symbolic shapes.

    We give the shapes 0 and 1 concrete values, while all other shapes
    are symbolic sympy formulas.
    """
    output = []
    for x, y in itertools.zip_longest(reversed(a), reversed(b), fillvalue=sympy.S.One):
        if V.graph.sizevars.shape_env.evaluate_expr(
            sympy.Eq(y, 1), size_oblivious=True
        ):
            output.append(x)
        elif V.graph.sizevars.shape_env.evaluate_expr(
            sympy.Eq(x, 1), size_oblivious=True
        ):
            output.append(y)
        else:
            V.graph.sizevars.guard_equals(x, y)
            if len(sympy.expand(y).free_symbols) < len(sympy.expand(x).free_symbols):
                output.append(y)  # prefer shorter formula
            else:
                output.append(x)
    return tuple(reversed(output))

def ceildiv(
    numer: Union[int, sympy.Expr], denom: Union[int, sympy.Expr]
) -> Union[int, sympy.Expr]:
    if isinstance(numer, sympy.Expr) or isinstance(denom, sympy.Expr):
        return CeilDiv(sympy.sympify(numer), sympy.sympify(denom))
    # TODO: There is a bug in a call to this function, to repro:
    # python benchmarks/dynamo/huggingface.py --inductor -d cuda --accuracy
    # --amp --only YituTechConvBert --dynamic-shapes
    assert isinstance(numer, int) and isinstance(denom, int), (
        f"{numer}: {type(numer)}, {denom}: {type(denom)}"
    )
    return runtime_ceildiv(numer, denom)

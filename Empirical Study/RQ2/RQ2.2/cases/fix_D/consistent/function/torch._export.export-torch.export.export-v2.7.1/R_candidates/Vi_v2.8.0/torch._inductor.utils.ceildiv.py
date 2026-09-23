def ceildiv(
    number: Union[int, sympy.Expr], denom: Union[int, sympy.Expr]
) -> Union[int, sympy.Expr]:
    if isinstance(number, sympy.Expr) or isinstance(denom, sympy.Expr):
        return CeilDiv(sympy.sympify(number), sympy.sympify(denom))
    # TODO: There is a bug in a call to this function, to repro:
    # python benchmarks/dynamo/huggingface.py --inductor -d cuda --accuracy
    # --amp --only YituTechConvBert --dynamic-shapes
    assert isinstance(number, int) and isinstance(denom, int), (
        f"{number}: {type(number)}, {denom}: {type(denom)}"
    )
    return runtime_ceildiv(number, denom)

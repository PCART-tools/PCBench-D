def parse_as_list_of_expressions(
    *inputs: IntoExpr | Iterable[IntoExpr],
    __structify: bool = False,
    **named_inputs: IntoExpr,
) -> list[PyExpr]:
    """
    Parse multiple inputs into a list of expressions.

    Parameters
    ----------
    *inputs
        Inputs to be parsed as expressions, specified as positional arguments.
    **named_inputs
        Additional inputs to be parsed as expressions, specified as keyword arguments.
        The expressions will be renamed to the keyword used.
    __structify
        Convert multi-column expressions to a single struct expression.

    """
    exprs = _parse_regular_inputs(inputs, structify=__structify)
    if named_inputs:
        named_exprs = _parse_named_inputs(named_inputs, structify=__structify)
        exprs.extend(named_exprs)

    return exprs

def parse_as_expression(
    input: IntoExpr,
    *,
    str_as_lit: bool = False,
    structify: bool = False,
) -> PyExpr | Expr:
    """
    Parse a single input into an expression.

    Parameters
    ----------
    input
        The input to be parsed as an expression.
    str_as_lit
        Interpret string input as a string literal. If set to ``False`` (default),
        strings are parsed as column names.
    structify
        Convert multi-column expressions to a single struct expression.
    wrap
        Return an ``Expr`` object rather than a ``PyExpr`` object.

    """
    if isinstance(input, pl.Expr):
        expr = input
    elif isinstance(input, str) and not str_as_lit:
        expr = F.col(input)
        structify = False
    elif (
        isinstance(
            input, (int, float, str, bytes, pl.Series, datetime, date, time, timedelta)
        )
        or input is None
    ):
        expr = F.lit(input)
        structify = False
    elif isinstance(input, (list, tuple)):
        expr = F.lit(pl.Series("literal", [input]))
        structify = False
    else:
        raise TypeError(
            f"did not expect value {input!r} of type {type(input).__name__!r}"
            "\n\nTry disambiguating with `lit` or `col`."
        )

    if structify:
        expr = _structify_expression(expr)

    return expr._pyexpr

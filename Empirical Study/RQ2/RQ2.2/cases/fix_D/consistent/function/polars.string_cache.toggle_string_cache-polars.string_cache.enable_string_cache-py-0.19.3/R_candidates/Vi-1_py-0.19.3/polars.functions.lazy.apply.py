@deprecate_renamed_function("map_groups", version="0.19.0")
def apply(
    exprs: Sequence[str | Expr],
    function: Callable[[Sequence[Series]], Series | Any],
    return_dtype: PolarsDataType | None = None,
    *,
    returns_scalar: bool = True,
) -> Expr:
    """
    Apply a custom/user-defined function (UDF) in a GroupBy context.

    .. deprecated:: 0.19.0
        This function has been renamed to :func:`map_groups`.

    Parameters
    ----------
    exprs
        Input Series to f
    function
        Function to apply over the input
    return_dtype
        dtype of the output Series
    returns_scalar
        If the function returns a single scalar as output.

    Returns
    -------
    Expr
        Expression with the data type given by ``return_dtype``.

    """
    return map_groups(exprs, function, return_dtype, returns_scalar=returns_scalar)

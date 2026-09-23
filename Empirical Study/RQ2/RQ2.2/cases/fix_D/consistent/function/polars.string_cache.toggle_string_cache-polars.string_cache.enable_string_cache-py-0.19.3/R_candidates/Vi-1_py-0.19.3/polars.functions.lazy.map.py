@deprecate_renamed_function("map_batches", version="0.19.0")
def map(
    exprs: Sequence[str] | Sequence[Expr],
    function: Callable[[Sequence[Series]], Series],
    return_dtype: PolarsDataType | None = None,
) -> Expr:
    """
    Map a custom function over multiple columns/expressions.

    .. deprecated:: 0.19.0
        This function has been renamed to :func:`map_batches`.

    Parameters
    ----------
    exprs
        Input Series to f
    function
        Function to apply over the input
    return_dtype
        dtype of the output Series

    Returns
    -------
    Expr
        Expression with the data type given by ``return_dtype``.

    """
    return map_batches(exprs, function, return_dtype)

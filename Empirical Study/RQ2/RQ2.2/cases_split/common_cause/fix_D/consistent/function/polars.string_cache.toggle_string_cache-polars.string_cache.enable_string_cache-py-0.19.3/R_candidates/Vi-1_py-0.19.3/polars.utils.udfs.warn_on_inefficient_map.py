def warn_on_inefficient_map(
    function: Callable[[Any], Any], columns: list[str], map_target: MapTarget
) -> None:
    """
    Generate ``PolarsInefficientMapWarning`` on poor usage of a ``map`` function.

    Parameters
    ----------
    function
        The function passed to ``map``.
    columns
        The column names of the original object; in the case of an ``Expr`` this
        will be a list of length 1 containing the expression's root name.
    map_target
        The target of the ``map`` call. One of ``"expr"``, ``"frame"``,
        or ``"series"``.
    """
    if map_target == "frame":
        raise NotImplementedError("TODO: 'frame' map-function parsing")

    # note: we only consider simple functions with a single col/param
    if not (col := columns and columns[0]):
        return None

    # the parser introspects function bytecode to determine if we can
    # rewrite as a much more optimal native polars expression instead
    parser = BytecodeParser(function, map_target)
    if parser.can_attempt_rewrite():
        parser.warn(col)
    else:
        # handle bare numpy/json functions
        module, suggestion = _is_raw_function(function)
        if module and suggestion:
            fn = function.__name__
            parser.warn(
                col,
                suggestion_override=f'pl.col("{col}").{suggestion}',
                udf_override=fn if module == "builtins" else f"{module}.{fn}",
            )

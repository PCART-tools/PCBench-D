def _create_col(
    name: str | PolarsDataType | Iterable[str] | Iterable[PolarsDataType],
    *more_names: str | PolarsDataType,
) -> Expr:
    """Create one or more column expressions representing column(s) in a DataFrame."""
    if more_names:
        if isinstance(name, str):
            names_str = [name]
            names_str.extend(more_names)  # type: ignore[arg-type]
            return wrap_expr(plr.cols(names_str))
        elif is_polars_dtype(name):
            dtypes = [name]
            dtypes.extend(more_names)  # type: ignore[arg-type]
            return wrap_expr(plr.dtype_cols(dtypes))
        else:
            msg = (
                "invalid input for `col`"
                f"\n\nExpected `str` or `DataType`, got {type(name).__name__!r}."
            )
            raise TypeError(msg)

    if isinstance(name, str):
        return wrap_expr(plr.col(name))
    elif is_polars_dtype(name):
        return wrap_expr(plr.dtype_cols([name]))
    elif isinstance(name, Iterable):
        names = list(name)
        if not names:
            return wrap_expr(plr.cols(names))

        item = names[0]
        if isinstance(item, str):
            return wrap_expr(plr.cols(names))
        elif is_polars_dtype(item):
            return wrap_expr(plr.dtype_cols(names))
        else:
            msg = (
                "invalid input for `col`"
                "\n\nExpected iterable of type `str` or `DataType`,"
                f" got iterable of type {type(item).__name__!r}."
            )
            raise TypeError(msg)
    else:
        msg = (
            "invalid input for `col`"
            f"\n\nExpected `str` or `DataType`, got {type(name).__name__!r}."
        )
        raise TypeError(msg)

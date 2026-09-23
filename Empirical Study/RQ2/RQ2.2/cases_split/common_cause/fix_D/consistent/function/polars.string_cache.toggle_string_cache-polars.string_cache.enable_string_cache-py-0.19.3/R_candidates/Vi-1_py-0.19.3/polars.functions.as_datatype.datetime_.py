def datetime_(
    year: int | IntoExpr,
    month: int | IntoExpr,
    day: int | IntoExpr,
    hour: int | IntoExpr | None = None,
    minute: int | IntoExpr | None = None,
    second: int | IntoExpr | None = None,
    microsecond: int | IntoExpr | None = None,
    *,
    time_unit: TimeUnit = "us",
    time_zone: str | None = None,
    use_earliest: bool | None = None,
    ambiguous: Ambiguous | Expr = "raise",
) -> Expr:
    """
    Create a Polars literal expression of type Datetime.

    Parameters
    ----------
    year
        Column or literal.
    month
        Column or literal, ranging from 1-12.
    day
        Column or literal, ranging from 1-31.
    hour
        Column or literal, ranging from 0-23.
    minute
        Column or literal, ranging from 0-59.
    second
        Column or literal, ranging from 0-59.
    microsecond
        Column or literal, ranging from 0-999999.
    time_unit : {'us', 'ms', 'ns'}
        Time unit of the resulting expression.
    time_zone
        Time zone of the resulting expression.
    use_earliest
        Determine how to deal with ambiguous datetimes:

        - ``None`` (default): raise
        - ``True``: use the earliest datetime
        - ``False``: use the latest datetime

        .. deprecated:: 0.19.0
            Use `ambiguous` instead
    ambiguous
        Determine how to deal with ambiguous datetimes:

        - ``'raise'`` (default): raise
        - ``'earliest'``: use the earliest datetime
        - ``'latest'``: use the latest datetime


    Returns
    -------
    Expr
        Expression of data type :class:`Datetime`.

    """
    ambiguous = parse_as_expression(
        rename_use_earliest_to_ambiguous(use_earliest, ambiguous), str_as_lit=True
    )
    year_expr = parse_as_expression(year)
    month_expr = parse_as_expression(month)
    day_expr = parse_as_expression(day)

    if hour is not None:
        hour = parse_as_expression(hour)
    if minute is not None:
        minute = parse_as_expression(minute)
    if second is not None:
        second = parse_as_expression(second)
    if microsecond is not None:
        microsecond = parse_as_expression(microsecond)

    return wrap_expr(
        plr.datetime(
            year_expr,
            month_expr,
            day_expr,
            hour,
            minute,
            second,
            microsecond,
            time_unit,
            time_zone,
            ambiguous,
        )
    )

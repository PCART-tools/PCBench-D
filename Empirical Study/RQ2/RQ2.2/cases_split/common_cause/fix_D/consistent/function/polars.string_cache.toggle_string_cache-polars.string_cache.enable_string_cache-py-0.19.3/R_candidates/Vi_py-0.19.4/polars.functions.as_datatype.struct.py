def struct(
    *exprs: IntoExpr | Iterable[IntoExpr],
    schema: SchemaDict | None = None,
    eager: bool = False,
    **named_exprs: IntoExpr,
) -> Expr | Series:
    """
    Collect columns into a struct column.

    Parameters
    ----------
    *exprs
        Column(s) to collect into a struct column, specified as positional arguments.
        Accepts expression input. Strings are parsed as column names,
        other non-expression inputs are parsed as literals.
    schema
        Optional schema that explicitly defines the struct field dtypes. If no columns
        or expressions are provided, schema keys are used to define columns.
    eager
        Evaluate immediately and return a ``Series``. If set to ``False`` (default),
        return an expression instead.
    **named_exprs
        Additional columns to collect into the struct column, specified as keyword
        arguments. The columns will be renamed to the keyword used.

    Examples
    --------
    Collect all columns of a dataframe into a struct by passing ``pl.all()``.

    >>> df = pl.DataFrame(
    ...     {
    ...         "int": [1, 2],
    ...         "str": ["a", "b"],
    ...         "bool": [True, None],
    ...         "list": [[1, 2], [3]],
    ...     }
    ... )
    >>> df.select(pl.struct(pl.all()).alias("my_struct"))
    shape: (2, 1)
    ┌─────────────────────┐
    │ my_struct           │
    │ ---                 │
    │ struct[4]           │
    ╞═════════════════════╡
    │ {1,"a",true,[1, 2]} │
    │ {2,"b",null,[3]}    │
    └─────────────────────┘

    Collect selected columns into a struct by either passing a list of columns, or by
    specifying each column as a positional argument.

    >>> df.select(pl.struct("int", False).alias("my_struct"))
    shape: (2, 1)
    ┌───────────┐
    │ my_struct │
    │ ---       │
    │ struct[2] │
    ╞═══════════╡
    │ {1,false} │
    │ {2,false} │
    └───────────┘

    Use keyword arguments to easily name each struct field.

    >>> df.select(pl.struct(p="int", q="bool").alias("my_struct")).schema
    {'my_struct': Struct([Field('p', Int64), Field('q', Boolean)])}

    """
    pyexprs = parse_as_list_of_expressions(*exprs, **named_exprs)
    expr = wrap_expr(plr.as_struct(pyexprs))

    if schema:
        if not exprs:
            # no columns or expressions provided; create one from schema keys
            expr = wrap_expr(
                plr.as_struct(parse_as_list_of_expressions(list(schema.keys())))
            )
        expr = expr.cast(Struct(schema), strict=False)

    if eager:
        return F.select(expr).to_series()
    else:
        return expr

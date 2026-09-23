def columns(
    cols: int | Sequence[str] | None = None,
    *,
    dtype: OneOrMoreDataTypes | None = None,
    min_cols: int | None = 0,
    max_cols: int | None = MAX_COLS,
    unique: bool = False,
) -> list[column]:
    """
    Define multiple columns for use with the @dataframes strategy.

    Generate a fixed sequence of `column` objects suitable for passing to the
    @dataframes strategy, or using standalone (note that this function is not itself
    a strategy).

    Notes
    -----
    Additional control is available by creating a sequence of columns explicitly,
    using the `column` class (an especially useful option is to override the default
    data-generating strategy for a given col/dtype).

    Parameters
    ----------
    cols : {int, [str]}, optional
        integer number of cols to create, or explicit list of column names. if
        omitted a random number of columns (between mincol and max_cols) are
        created.
    dtype : PolarsDataType, optional
        a single dtype for all cols, or list of dtypes (the same length as `cols`).
        if omitted, each generated column is assigned a random dtype.
    min_cols : int, optional
        if not passing an exact size, can set a minimum here (defaults to 0).
    max_cols : int, optional
        if not passing an exact size, can set a maximum value here (defaults to
        MAX_COLS).
    unique : bool, optional
        indicate if the values generated for these columns should be unique
        (per-column).

    Examples
    --------
    >>> from polars.testing.parametric import columns, dataframes
    >>> from hypothesis import given
    >>>
    >>> @given(dataframes(columns(["x", "y", "z"], unique=True)))
    ... def test_unique_xyz(df: pl.DataFrame) -> None:
    ...     assert_something(df)

    Note, as 'columns' creates a list of native polars column definitions it can
    also be used independently of parametric/hypothesis tests:

    >>> from string import punctuation
    >>>
    >>> def test_special_char_colname_init() -> None:
    ...     df = pl.DataFrame(schema=[(c.name, c.dtype) for c in columns(punctuation)])
    ...     assert len(cols) == len(df.columns)
    ...     assert 0 == len(df.rows())
    ...

    """
    # create/assign named columns
    if cols is None:
        cols = random.randint(
            a=min_cols or 0,
            b=max_cols or MAX_COLS,
        )
    if isinstance(cols, int):
        names: list[str] = [f"col{n}" for n in range(cols)]
    else:
        names = list(cols)

    if isinstance(dtype, Sequence):
        if len(dtype) != len(names):
            raise InvalidArgument(f"given {len(dtype)} dtypes for {len(names)} names")
        dtypes = list(dtype)
    elif dtype is None:
        dtypes = [random.choice(strategy_dtypes) for _ in range(len(names))]
    elif is_polars_dtype(dtype):
        dtypes = [dtype] * len(names)
    else:
        raise InvalidArgument(f"{dtype!r} is not a valid polars datatype")

    # init list of named/typed columns
    return [column(name=nm, dtype=tp, unique=unique) for nm, tp in zip(names, dtypes)]

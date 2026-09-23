def from_repr(tbl: str) -> DataFrame | Series:
    """
    Utility function that reconstructs a DataFrame or Series from the object's repr.

    Parameters
    ----------
    tbl
        A string containing a polars DataFrame or Series repr; does not need
        to be trimmed of whitespace (or leading prompts) as the repr will be
        found/extracted automatically.

    Notes
    -----
    This function handles the default UTF8_FULL and UTF8_FULL_CONDENSED DataFrame
    tables (with or without rounded corners). Truncated columns/rows are omitted,
    wrapped headers are accounted for, and dtypes automatically identified.

    Currently compound/nested dtypes such as List and Struct are not supported;
    neither are Object dtypes.

    See Also
    --------
    polars.DataFrame.to_init_repr
    polars.Series.to_init_repr

    Examples
    --------
    From DataFrame table repr:

    >>> df = pl.from_repr(
    ...     '''
    ...     Out[3]:
    ...     shape: (1, 5)
    ...     ┌───────────┬────────────┬───┬───────┬────────────────────────────────┐
    ...     │ source_ac ┆ source_cha ┆ … ┆ ident ┆ timestamp                      │
    ...     │ tor_id    ┆ nnel_id    ┆   ┆ ---   ┆ ---                            │
    ...     │ ---       ┆ ---        ┆   ┆ str   ┆ datetime[μs, Asia/Tokyo]       │
    ...     │ i32       ┆ i64        ┆   ┆       ┆                                │
    ...     ╞═══════════╪════════════╪═══╪═══════╪════════════════════════════════╡
    ...     │ 123456780 ┆ 9876543210 ┆ … ┆ a:b:c ┆ 2023-03-25 10:56:59.663053 JST │
    ...     │ …         ┆ …          ┆ … ┆ …     ┆ …                              │
    ...     │ 803065983 ┆ 2055938745 ┆ … ┆ x:y:z ┆ 2023-03-25 12:38:18.050545 JST │
    ...     └───────────┴────────────┴───┴───────┴────────────────────────────────┘
    ... '''
    ... )
    >>> df
    shape: (2, 4)
    ┌─────────────────┬───────────────────┬───────┬────────────────────────────────┐
    │ source_actor_id ┆ source_channel_id ┆ ident ┆ timestamp                      │
    │ ---             ┆ ---               ┆ ---   ┆ ---                            │
    │ i32             ┆ i64               ┆ str   ┆ datetime[μs, Asia/Tokyo]       │
    ╞═════════════════╪═══════════════════╪═══════╪════════════════════════════════╡
    │ 123456780       ┆ 9876543210        ┆ a:b:c ┆ 2023-03-25 10:56:59.663053 JST │
    │ 803065983       ┆ 2055938745        ┆ x:y:z ┆ 2023-03-25 12:38:18.050545 JST │
    └─────────────────┴───────────────────┴───────┴────────────────────────────────┘
    >>> df.schema
    {'source_actor_id': Int32,
     'source_channel_id': Int64,
     'ident': Utf8,
     'timestamp': Datetime(time_unit='us', time_zone='Asia/Tokyo')}

    From Series repr:

    >>> srs = pl.from_repr(
    ...     '''
    ...     shape: (3,)
    ...     Series: 's' [bool]
    ...     [
    ...        true
    ...        false
    ...        true
    ...     ]
    ...     '''
    ... )
    >>> srs.to_list()
    [True, False, True]

    """
    # find DataFrame table...
    m = re.search(r"([┌╭].*?[┘╯])", tbl, re.DOTALL)
    if m is not None:
        return _from_dataframe_repr(m)

    # ...or Series in the given string
    m = re.search(
        pattern=r"(?:shape: (\(\d+,\))\n.*?)?Series:\s+([^\n]+)\s+\[([^\n]+)](.*)",
        string=tbl,
        flags=re.DOTALL,
    )
    if m is not None:
        return _from_series_repr(m)

    raise ValueError("input string does not contain DataFrame or Series")

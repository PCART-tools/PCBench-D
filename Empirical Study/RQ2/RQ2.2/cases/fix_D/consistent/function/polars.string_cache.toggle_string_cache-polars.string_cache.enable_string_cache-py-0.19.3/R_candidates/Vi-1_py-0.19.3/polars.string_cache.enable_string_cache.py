def enable_string_cache(enable: bool) -> None:  # noqa: FBT001
    """
    Enable (or disable) the global string cache.

    This ensures that casts to Categorical dtypes will have
    the same category values when string values are equal.

    Parameters
    ----------
    enable
        Enable or disable the global string cache.

    Examples
    --------
    >>> pl.enable_string_cache(True)
    >>> df1 = pl.DataFrame(
    ...     data={"color": ["red", "green", "blue", "orange"], "value": [1, 2, 3, 4]},
    ...     schema={"color": pl.Categorical, "value": pl.UInt8},
    ... )
    >>> df2 = pl.DataFrame(
    ...     data={
    ...         "color": ["yellow", "green", "orange", "black", "red"],
    ...         "char": ["a", "b", "c", "d", "e"],
    ...     },
    ...     schema={"color": pl.Categorical, "char": pl.Utf8},
    ... )
    >>> df_join = df1.join(df2, how="inner", on="color")
    >>> df_join
    shape: (3, 3)
    ┌────────┬───────┬──────┐
    │ color  ┆ value ┆ char │
    │ ---    ┆ ---   ┆ ---  │
    │ cat    ┆ u8    ┆ str  │
    ╞════════╪═══════╪══════╡
    │ green  ┆ 2     ┆ b    │
    │ orange ┆ 4     ┆ c    │
    │ red    ┆ 1     ┆ e    │
    └────────┴───────┴──────┘

    """
    _enable_string_cache(enable)

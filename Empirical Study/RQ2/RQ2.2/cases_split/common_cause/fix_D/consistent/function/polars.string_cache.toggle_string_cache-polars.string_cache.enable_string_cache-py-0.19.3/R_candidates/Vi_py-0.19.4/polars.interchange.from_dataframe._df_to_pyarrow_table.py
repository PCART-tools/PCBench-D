def _df_to_pyarrow_table(df: Any, *, allow_copy: bool = False) -> pa.Table:
    if not _PYARROW_AVAILABLE or parse_version(pa.__version__) < parse_version("11"):
        raise ImportError(
            "pyarrow>=11.0.0 is required for converting a dataframe interchange object"
            " to a Polars dataframe"
        )

    import pyarrow.interchange  # noqa: F401

    if not allow_copy:
        return _df_to_pyarrow_table_zero_copy(df)

    return pa.interchange.from_dataframe(df, allow_copy=True)

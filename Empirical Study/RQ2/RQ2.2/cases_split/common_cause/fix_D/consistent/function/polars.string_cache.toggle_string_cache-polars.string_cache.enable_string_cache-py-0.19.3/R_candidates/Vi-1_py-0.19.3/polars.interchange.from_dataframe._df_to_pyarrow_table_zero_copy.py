def _df_to_pyarrow_table_zero_copy(df: Any) -> pa.Table:
    dfi = df.__dataframe__(allow_copy=False)
    if _dfi_contains_categorical_data(dfi):
        raise TypeError(
            "Polars can not currently guarantee zero-copy conversion from Arrow for categorical columns"
            "\n\nSet `allow_copy=True` or cast categorical columns to string first."
        )

    if isinstance(df, pa.Table):
        return df
    elif isinstance(df, pa.RecordBatch):
        return pa.Table.from_batches([df])
    else:
        return pa.interchange.from_dataframe(dfi, allow_copy=False)

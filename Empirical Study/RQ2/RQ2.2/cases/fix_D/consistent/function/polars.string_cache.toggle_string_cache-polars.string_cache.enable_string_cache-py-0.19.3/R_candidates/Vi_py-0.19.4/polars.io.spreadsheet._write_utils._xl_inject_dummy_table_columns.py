def _xl_inject_dummy_table_columns(
    df: DataFrame, options: dict[str, Any], dtype: PolarsDataType | None = None
) -> DataFrame:
    """Insert dummy frame columns in order to create empty/named table columns."""
    df_original_columns = set(df.columns)
    df_select_cols = df.columns.copy()
    cast_lookup = {}

    for col, definition in options.items():
        if col in df_original_columns:
            raise DuplicateError(f"cannot create a second {col!r} column")
        elif not isinstance(definition, dict):
            df_select_cols.append(col)
        else:
            cast_lookup[col] = definition.get("return_dtype")
            insert_before = definition.get("insert_before")
            insert_after = definition.get("insert_after")

            if insert_after is None and insert_before is None:
                df_select_cols.append(col)
            else:
                insert_idx = (
                    df_select_cols.index(insert_after) + 1  # type: ignore[arg-type]
                    if insert_before is None
                    else df_select_cols.index(insert_before)
                )
                df_select_cols.insert(insert_idx, col)

    df = df.select(
        [
            (
                col
                if col in df_original_columns
                else (
                    F.lit(None).cast(
                        cast_lookup.get(col, dtype)  # type:ignore[arg-type]
                    )
                    if dtype or (col in cast_lookup and cast_lookup[col] is not None)
                    else F.lit(None)
                ).alias(col)
            )
            for col in df_select_cols
        ]
    )
    return df

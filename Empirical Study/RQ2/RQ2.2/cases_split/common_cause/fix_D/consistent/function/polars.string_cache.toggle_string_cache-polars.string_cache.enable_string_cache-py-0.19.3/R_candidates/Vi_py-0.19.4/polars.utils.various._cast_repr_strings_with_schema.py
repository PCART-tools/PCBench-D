def _cast_repr_strings_with_schema(
    df: DataFrame, schema: dict[str, PolarsDataType | None]
) -> DataFrame:
    """
    Utility function to cast table repr/string values into frame-native types.

    Parameters
    ----------
    df
        Dataframe containing string-repr column data.
    schema
        DataFrame schema containing the desired end-state types.

    Notes
    -----
    Table repr strings are less strict (or different) than equivalent CSV data, so need
    special handling; as this function is only used for reprs, parsing is flexible.

    """
    tp: PolarsDataType | None
    if not df.is_empty():
        for tp in df.schema.values():
            if tp != Utf8:
                raise TypeError(
                    f"DataFrame should contain only Utf8 string repr data; found {tp!r}"
                )

    # duration string scaling
    ns_sec = 1_000_000_000
    duration_scaling = {
        "ns": 1,
        "us": 1_000,
        "µs": 1_000,
        "ms": 1_000_000,
        "s": ns_sec,
        "m": ns_sec * 60,
        "h": ns_sec * 60 * 60,
        "d": ns_sec * 3_600 * 24,
        "w": ns_sec * 3_600 * 24 * 7,
    }

    # identify duration units and convert to nanoseconds
    def str_duration_(td: str | None) -> int | None:
        return (
            None
            if td is None
            else sum(
                int(value) * duration_scaling[unit.strip()]
                for value, unit in re.findall(r"(\d+)(\D+)", td)
            )
        )

    cast_cols = {}
    for c, tp in schema.items():
        if tp is not None:
            if tp.base_type() == Datetime:
                tp_base = Datetime(tp.time_unit)  # type: ignore[union-attr]
                d = F.col(c).str.replace(r"[A-Z ]+$", "")
                cast_cols[c] = (
                    F.when(d.str.lengths() == 19)
                    .then(d + ".000000000")
                    .otherwise(d + "000000000")
                    .str.slice(0, 29)
                    .str.strptime(tp_base, "%Y-%m-%d %H:%M:%S.%9f")
                )
                if getattr(tp, "time_zone", None) is not None:
                    cast_cols[c] = cast_cols[c].dt.replace_time_zone(tp.time_zone)  # type: ignore[union-attr]
            elif tp == Date:
                cast_cols[c] = F.col(c).str.strptime(tp, "%Y-%m-%d")  # type: ignore[arg-type]
            elif tp == Time:
                cast_cols[c] = (
                    F.when(F.col(c).str.lengths() == 8)
                    .then(F.col(c) + ".000000000")
                    .otherwise(F.col(c) + "000000000")
                    .str.slice(0, 18)
                    .str.strptime(tp, "%H:%M:%S.%9f")  # type: ignore[arg-type]
                )
            elif tp == Duration:
                cast_cols[c] = (
                    F.col(c)
                    .apply(str_duration_, return_dtype=Int64)
                    .cast(Duration("ns"))
                    .cast(tp)
                )
            elif tp == Boolean:
                cast_cols[c] = F.col(c).map_dict(
                    {"true": True, "false": False}, return_dtype=Boolean
                )
            elif tp != df.schema[c]:
                cast_cols[c] = F.col(c).cast(tp)

    return df.with_columns(**cast_cols) if cast_cols else df

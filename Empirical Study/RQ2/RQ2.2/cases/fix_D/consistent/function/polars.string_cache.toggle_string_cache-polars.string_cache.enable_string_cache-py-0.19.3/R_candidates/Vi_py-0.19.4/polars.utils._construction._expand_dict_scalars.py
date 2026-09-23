def _expand_dict_scalars(
    data: Mapping[str, Sequence[object] | Mapping[str, Sequence[object]] | Series],
    *,
    schema_overrides: SchemaDict | None = None,
    order: Sequence[str] | None = None,
    nan_to_null: bool = False,
) -> dict[str, Series]:
    """Expand any scalar values in dict data (propagate literal as array)."""
    updated_data = {}
    if data:
        dtypes = schema_overrides or {}
        data = _expand_dict_data(data, dtypes)
        array_len = max((arrlen(val) or 0) for val in data.values())
        if array_len > 0:
            for name, val in data.items():
                dtype = dtypes.get(name)
                if isinstance(val, dict) and dtype != Struct:
                    updated_data[name] = pl.DataFrame(val).to_struct(name)

                elif isinstance(val, pl.Series):
                    s = val.rename(name) if name != val.name else val
                    if dtype and dtype != s.dtype:
                        s = s.cast(dtype)
                    updated_data[name] = s

                elif arrlen(val) is not None or _is_generator(val):
                    updated_data[name] = pl.Series(
                        name=name, values=val, dtype=dtype, nan_to_null=nan_to_null
                    )
                elif val is None or isinstance(  # type: ignore[redundant-expr]
                    val, (int, float, str, bool, date, datetime, time, timedelta)
                ):
                    updated_data[name] = pl.Series(
                        name=name, values=[val], dtype=dtype
                    ).extend_constant(val, array_len - 1)
                else:
                    updated_data[name] = pl.Series(
                        name=name, values=[val] * array_len, dtype=dtype
                    )

        elif all((arrlen(val) == 0) for val in data.values()):
            for name, val in data.items():
                updated_data[name] = pl.Series(name, values=val, dtype=dtypes.get(name))

        elif all((arrlen(val) is None) for val in data.values()):
            for name, val in data.items():
                updated_data[name] = pl.Series(
                    name,
                    values=(val if _is_generator(val) else [val]),
                    dtype=dtypes.get(name),
                )
    if order and list(updated_data) != order:
        return {col: updated_data.pop(col) for col in order}
    return updated_data

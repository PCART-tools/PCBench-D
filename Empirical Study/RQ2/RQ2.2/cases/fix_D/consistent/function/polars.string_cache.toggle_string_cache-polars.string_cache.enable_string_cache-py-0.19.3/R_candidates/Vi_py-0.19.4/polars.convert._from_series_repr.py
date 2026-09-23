def _from_series_repr(m: re.Match[str]) -> Series:
    """Reconstruct a Series from a regex-matched series repr."""
    from polars.datatypes.convert import dtype_short_repr_to_dtype

    shape = m.groups()[0]
    name = m.groups()[1][1:-1]
    length = int(shape[1:-2] if shape else -1)
    dtype = dtype_short_repr_to_dtype(m.groups()[2])

    if length == 0:
        string_values = []
    else:
        string_values = [
            v.strip()
            for v in re.findall(r"[\s>#]*(?:\t|\s{4,})([^\n]*)\n", m.groups()[-1])
        ]
        if string_values == ["[", "]"]:
            string_values = []
        elif string_values and string_values[0].lstrip("#> ") == "[":
            string_values = string_values[1:]

    values = string_values[:length] if length > 0 else string_values
    values = [(None if v == "null" else v) for v in values if v not in ("…", "...")]

    if not values:
        return pl.Series(name=name, values=values, dtype=dtype)
    else:
        srs = pl.Series(name=name, values=values, dtype=Utf8)
        if dtype is None:
            return srs
        elif dtype in (Categorical, Utf8):
            return srs.str.replace('^"(.*)"$', r"$1").cast(dtype)

        return _cast_repr_strings_with_schema(
            srs.to_frame(), schema={srs.name: dtype}
        ).to_series()

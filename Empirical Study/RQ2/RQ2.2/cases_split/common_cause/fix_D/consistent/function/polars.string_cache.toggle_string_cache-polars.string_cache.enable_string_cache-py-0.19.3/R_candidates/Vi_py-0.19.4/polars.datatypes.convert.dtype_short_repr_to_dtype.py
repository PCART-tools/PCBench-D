def dtype_short_repr_to_dtype(dtype_string: str | None) -> PolarsDataType | None:
    """Map a PolarsDataType short repr (eg: 'i64', 'list[str]') back into a dtype."""
    if dtype_string is None:
        return None
    m = re.match(r"^(\w+)(?:\[(.+)\])?$", dtype_string)
    if m is None:
        return None

    dtype_base, subtype = m.groups()
    dtype = DataTypeMappings.REPR_TO_DTYPE.get(dtype_base)
    if dtype and subtype:
        # TODO: further-improve handling for nested types (such as List,Struct)
        try:
            if dtype == Decimal:
                subtype = (None, int(subtype))
            else:
                subtype = (
                    s.strip("'\" ") for s in subtype.replace("μs", "us").split(",")
                )
            return dtype(*subtype)  # type: ignore[operator]
        except ValueError:
            pass
    return dtype

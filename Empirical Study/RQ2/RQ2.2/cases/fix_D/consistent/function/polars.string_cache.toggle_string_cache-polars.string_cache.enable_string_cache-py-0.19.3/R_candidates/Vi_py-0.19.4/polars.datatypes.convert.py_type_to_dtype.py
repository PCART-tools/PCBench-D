def py_type_to_dtype(
    data_type: Any, *, raise_unmatched: bool = True, allow_strings: bool = False
) -> PolarsDataType | None:
    """Convert a Python dtype (or type annotation) to a Polars dtype."""
    if isinstance(data_type, ForwardRef):
        annotation = data_type.__forward_arg__
        data_type = (
            PY_STR_TO_DTYPE.get(
                re.sub(r"(^None \|)|(\| None$)", "", annotation).strip(), data_type
            )
            if isinstance(annotation, str)  # type: ignore[redundant-expr]
            else annotation
        )
    elif type(data_type).__name__ == "InitVar":
        data_type = data_type.type

    if is_polars_dtype(data_type):
        return data_type

    elif isinstance(data_type, (OptionType, UnionType)):
        # not exhaustive; handles the common "type | None" case, but
        # should probably pick appropriate supertype when n_types > 1?
        possible_types = [tp for tp in get_args(data_type) if tp is not NoneType]
        if len(possible_types) == 1:
            data_type = possible_types[0]

    elif allow_strings and isinstance(data_type, str):
        data_type = DataTypeMappings.REPR_TO_DTYPE.get(
            re.sub(r"^(?:dataclasses\.)?InitVar\[(.+)\]$", r"\1", data_type),
            data_type,
        )
        if is_polars_dtype(data_type):
            return data_type
    try:
        return _map_py_type_to_dtype(data_type)
    except (KeyError, TypeError):  # pragma: no cover
        if not raise_unmatched:
            return None
        raise ValueError(
            f"cannot infer dtype from {data_type!r} (type: {type(data_type).__name__!r})"
        ) from None

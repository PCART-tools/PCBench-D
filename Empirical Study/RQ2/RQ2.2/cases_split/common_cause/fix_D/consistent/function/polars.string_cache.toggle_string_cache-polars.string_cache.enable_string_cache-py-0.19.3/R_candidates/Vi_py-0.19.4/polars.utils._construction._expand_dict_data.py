def _expand_dict_data(
    data: Mapping[str, Sequence[object] | Mapping[str, Sequence[object]] | Series],
    dtypes: SchemaDict,
) -> Mapping[str, Sequence[object] | Mapping[str, Sequence[object]] | Series]:
    """
    Expand any unsized generators/iterators.

    (Note that `range` is sized, and will take a fast-path on Series init).
    """
    expanded_data = {}
    for name, val in data.items():
        expanded_data[name] = (
            pl.Series(name, val, dtypes.get(name)) if _is_generator(val) else val
        )
    return expanded_data

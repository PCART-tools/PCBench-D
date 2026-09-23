def _defaultdict_flatten_with_keys(
    d: defaultdict[Any, T]
) -> tuple[list[tuple[KeyEntry, T]], Context]:
    values, context = _defaultdict_flatten(d)
    _, dict_context = context
    return [(MappingKey(k), v) for k, v in zip(dict_context, values)], context

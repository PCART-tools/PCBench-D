def _ordereddict_flatten_with_keys(
    d: OrderedDict[Any, T]
) -> tuple[list[tuple[KeyEntry, T]], Context]:
    values, context = _ordereddict_flatten(d)
    return [(MappingKey(k), v) for k, v in zip(context, values)], context

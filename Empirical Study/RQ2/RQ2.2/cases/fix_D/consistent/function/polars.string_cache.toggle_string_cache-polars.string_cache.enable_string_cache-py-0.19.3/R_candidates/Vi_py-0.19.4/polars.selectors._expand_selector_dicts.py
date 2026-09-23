def _expand_selector_dicts(
    df: DataFrame,
    d: Mapping[Any, Any] | None,
    *,
    expand_keys: bool,
    expand_values: bool,
    tuple_keys: bool = False,
) -> dict[str, Any]:
    """Expand dict key/value selectors into their underlying column names."""
    expanded = {}
    for key, value in (d or {}).items():
        if expand_values and is_selector(value):
            expanded[key] = expand_selector(df, selector=value)
            value = expanded[key]
        if expand_keys and is_selector(key):
            cols = expand_selector(df, selector=key)
            if tuple_keys:
                expanded[cols] = value
            else:
                expanded.update({c: value for c in cols})
        else:
            expanded[key] = value
    return expanded

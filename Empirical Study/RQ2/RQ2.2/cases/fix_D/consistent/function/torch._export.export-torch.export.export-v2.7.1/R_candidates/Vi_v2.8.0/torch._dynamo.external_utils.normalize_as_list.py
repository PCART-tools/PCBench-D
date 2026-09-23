def normalize_as_list(x: Any) -> list[Any]:
    if isinstance(x, tuple):
        return list(x)
    elif isinstance(x, list):
        return x
    return [x]

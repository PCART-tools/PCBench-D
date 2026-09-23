def empty_safe_aggregate(func, parts):
    parts2 = [p for p in parts if not eq_strict(p, no_result)]
    return empty_safe_apply(func, parts2)

def coerce_e(value):
    return value if isinstance(value, _E) else _E(value)

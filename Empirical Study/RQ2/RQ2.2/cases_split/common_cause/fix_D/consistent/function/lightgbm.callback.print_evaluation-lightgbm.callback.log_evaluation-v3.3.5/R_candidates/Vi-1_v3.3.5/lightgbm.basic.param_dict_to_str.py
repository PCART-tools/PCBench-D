def param_dict_to_str(data):
    """Convert Python dictionary to string, which is passed to C API."""
    if data is None or not data:
        return ""
    pairs = []
    for key, val in data.items():
        if isinstance(val, (list, tuple, set)) or is_numpy_1d_array(val):
            def to_string(x):
                if isinstance(x, list):
                    return f"[{','.join(map(str, x))}]"
                else:
                    return str(x)
            pairs.append(f"{key}={','.join(map(to_string, val))}")
        elif isinstance(val, (str, Path, NUMERIC_TYPES)) or is_numeric(val):
            pairs.append(f"{key}={val}")
        elif val is not None:
            raise TypeError(f'Unknown type of parameter:{key}, got:{type(val).__name__}')
    return ' '.join(pairs)

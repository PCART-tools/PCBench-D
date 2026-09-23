def parse_kwarg(kwarg_str):
    key, value = map(string.strip, kwarg_str.split("=", 1))
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            pass
    return key, value

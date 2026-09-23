def parse_kwarg(kwarg_str):
    key, value = kwarg_str.split('=')
    try:
        value = ast.literal_eval(value)
    except ValueError:
        pass
    return key, value

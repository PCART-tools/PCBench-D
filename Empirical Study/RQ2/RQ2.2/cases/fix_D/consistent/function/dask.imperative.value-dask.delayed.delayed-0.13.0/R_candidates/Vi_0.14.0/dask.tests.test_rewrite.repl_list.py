def repl_list(sd):
    x = sd['x']
    if isinstance(x, list):
        return x
    else:
        return (list, x)

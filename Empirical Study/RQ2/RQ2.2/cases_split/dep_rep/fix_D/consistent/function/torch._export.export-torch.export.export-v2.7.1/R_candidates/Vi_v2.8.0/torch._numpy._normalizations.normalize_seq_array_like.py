def normalize_seq_array_like(x, parm=None):
    return tuple(normalize_array_like(value) for value in x)

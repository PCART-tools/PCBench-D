def is_1d_list(data):
    """Check whether data is a 1-D list."""
    return isinstance(data, list) and (not data or is_numeric(data[0]))

def c_array(ctype, values):
    """Convert a Python array to C array."""
    return (ctype * len(values))(*values)

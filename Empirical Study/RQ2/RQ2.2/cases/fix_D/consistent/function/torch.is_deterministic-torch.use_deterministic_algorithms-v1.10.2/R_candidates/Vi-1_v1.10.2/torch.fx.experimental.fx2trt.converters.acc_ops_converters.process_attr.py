def process_attr(val, num_elem):
    if not isinstance(val, tuple):
        val = (val,) * num_elem
    return val

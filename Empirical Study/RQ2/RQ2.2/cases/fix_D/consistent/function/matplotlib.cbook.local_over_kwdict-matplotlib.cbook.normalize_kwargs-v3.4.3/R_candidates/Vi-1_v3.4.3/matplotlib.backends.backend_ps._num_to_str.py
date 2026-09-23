def _num_to_str(val):
    if isinstance(val, str):
        return val

    ival = int(val)
    if val == ival:
        return str(ival)

    s = "%1.3f" % val
    s = s.rstrip("0")
    s = s.rstrip(".")
    return s

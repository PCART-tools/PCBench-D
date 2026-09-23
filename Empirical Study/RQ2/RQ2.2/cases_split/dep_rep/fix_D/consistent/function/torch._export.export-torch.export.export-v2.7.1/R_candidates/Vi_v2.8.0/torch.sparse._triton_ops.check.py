def check(cond, msg):
    if not cond:
        raise ValueError(msg)

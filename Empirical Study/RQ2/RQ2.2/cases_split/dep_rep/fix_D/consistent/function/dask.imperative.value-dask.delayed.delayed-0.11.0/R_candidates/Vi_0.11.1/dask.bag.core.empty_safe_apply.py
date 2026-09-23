def empty_safe_apply(func, part):
    part = list(part)
    if part:
        return func(part)
    else:
        return no_result

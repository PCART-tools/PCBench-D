def empty_safe_apply(func, part):
    if isinstance(part, Iterator):
        try:
            _, part = peek(part)
            return func(part)
        except StopIteration:
            return no_result
    else:
        return func(part)

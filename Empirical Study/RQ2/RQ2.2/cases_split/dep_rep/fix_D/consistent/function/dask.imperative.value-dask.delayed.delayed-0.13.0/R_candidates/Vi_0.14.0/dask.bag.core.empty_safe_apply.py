def empty_safe_apply(func, part, is_last):
    if isinstance(part, Iterator):
        try:
            _, part = peek(part)
        except StopIteration:
            if not is_last:
                return no_result
        return func(part)
    elif not is_last and len(part) == 0:
        return no_result
    else:
        return func(part)

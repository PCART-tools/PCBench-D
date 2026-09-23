def strict_zip(*iterables, strict=True, **kwargs):
    if not strict:
        return original_zip(*iterables, **kwargs)

    length = len(iterables[0])
    for iterable in iterables[1:]:
        if len(iterable) != length:
            raise ValueError(
                "The iterables have different lengths and strict mode is enabled."
            )

    return original_zip(*iterables, **kwargs)

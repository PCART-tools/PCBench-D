class StatusCodeCompat:
    def __call__(self, *args, **kwargs):  # type: ignore
        message = "`httpx.StatusCode` is deprecated. Use `httpx.codes` instead."
        warnings.warn(message, DeprecationWarning)
        return codes(*args, **kwargs)

    def __getattr__(self, attr):  # type: ignore
        message = "`httpx.StatusCode` is deprecated. Use `httpx.codes` instead."
        warnings.warn(message, DeprecationWarning)
        return getattr(codes, attr)

    def __getitem__(self, item):  # type: ignore
        message = "`httpx.StatusCode` is deprecated. Use `httpx.codes` instead."
        warnings.warn(message, DeprecationWarning)
        return codes[item]

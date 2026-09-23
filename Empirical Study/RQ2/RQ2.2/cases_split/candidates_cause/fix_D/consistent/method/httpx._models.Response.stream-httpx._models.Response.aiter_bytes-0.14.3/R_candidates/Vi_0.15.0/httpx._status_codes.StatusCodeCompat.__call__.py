    def __call__(self, *args, **kwargs):  # type: ignore
        message = "`httpx.StatusCode` is deprecated. Use `httpx.codes` instead."
        warnings.warn(message, DeprecationWarning)
        return codes(*args, **kwargs)

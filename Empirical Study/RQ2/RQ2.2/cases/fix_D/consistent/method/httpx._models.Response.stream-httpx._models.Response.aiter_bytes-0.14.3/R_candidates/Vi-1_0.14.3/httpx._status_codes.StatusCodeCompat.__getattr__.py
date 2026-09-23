    def __getattr__(self, attr):  # type: ignore
        message = "`httpx.StatusCode` is deprecated. Use `httpx.codes` instead."
        warnings.warn(message, DeprecationWarning)
        return getattr(codes, attr)

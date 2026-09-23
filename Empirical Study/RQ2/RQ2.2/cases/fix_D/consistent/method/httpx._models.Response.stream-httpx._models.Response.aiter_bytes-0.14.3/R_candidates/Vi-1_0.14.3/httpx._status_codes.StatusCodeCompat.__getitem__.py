    def __getitem__(self, item):  # type: ignore
        message = "`httpx.StatusCode` is deprecated. Use `httpx.codes` instead."
        warnings.warn(message, DeprecationWarning)
        return codes[item]

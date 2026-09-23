    def __enter__(self):
        warnings.warn("Use async with instead", DeprecationWarning)
        return self

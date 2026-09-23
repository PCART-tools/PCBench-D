    @functools.lru_cache()  # Always return the same instance.
    def __new__(cls):
        self = object.__new__(cls)
        self._reinit()
        return self

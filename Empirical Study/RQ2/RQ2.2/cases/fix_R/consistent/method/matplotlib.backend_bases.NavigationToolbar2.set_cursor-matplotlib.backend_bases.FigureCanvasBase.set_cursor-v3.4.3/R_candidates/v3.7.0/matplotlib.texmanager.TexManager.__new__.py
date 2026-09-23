    @functools.lru_cache()  # Always return the same instance.
    def __new__(cls):
        Path(cls.texcache).mkdir(parents=True, exist_ok=True)
        return object.__new__(cls)

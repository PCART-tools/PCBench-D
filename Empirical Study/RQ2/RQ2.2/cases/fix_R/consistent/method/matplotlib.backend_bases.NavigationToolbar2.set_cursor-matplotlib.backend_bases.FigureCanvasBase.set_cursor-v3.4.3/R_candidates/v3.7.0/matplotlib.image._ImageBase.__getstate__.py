    def __getstate__(self):
        # Save some space on the pickle by not saving the cache.
        return {**super().__getstate__(), "_imcache": None}

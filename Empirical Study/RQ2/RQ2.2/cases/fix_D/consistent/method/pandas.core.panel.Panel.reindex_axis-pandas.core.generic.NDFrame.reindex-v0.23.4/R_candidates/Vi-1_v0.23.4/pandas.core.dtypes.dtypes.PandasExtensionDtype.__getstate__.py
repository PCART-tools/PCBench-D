    def __getstate__(self):
        # pickle support; we don't want to pickle the cache
        return {k: getattr(self, k, None) for k in self._metadata}

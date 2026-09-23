    @_api.deprecated("3.6", alternative="TexManager()")
    def get_texmanager(self):
        """Return the cached `~.texmanager.TexManager` instance."""
        if self._texmanager is None:
            self._texmanager = TexManager()
        return self._texmanager

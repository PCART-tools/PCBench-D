    def get_texmanager(self):
        """Return the `.TexManager` instance."""
        if self._texmanager is None:
            self._texmanager = TexManager()
        return self._texmanager

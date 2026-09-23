    def get_texmanager(self):
        """Return the cached `~.texmanager.TexManager` instance."""
        if self._texmanager is None:
            from matplotlib.texmanager import TexManager
            self._texmanager = TexManager()
        return self._texmanager

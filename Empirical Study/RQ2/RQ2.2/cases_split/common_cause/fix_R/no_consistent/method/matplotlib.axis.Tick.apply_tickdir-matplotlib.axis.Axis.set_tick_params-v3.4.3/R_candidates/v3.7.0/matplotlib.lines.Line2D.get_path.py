    def get_path(self):
        """Return the `~matplotlib.path.Path` associated with this line."""
        if self._invalidy or self._invalidx:
            self.recache()
        return self._path

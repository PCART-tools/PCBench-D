    def get_path(self):
        """
        Return the :class:`~matplotlib.path.Path` object associated
        with this line.
        """
        if self._invalidy or self._invalidx:
            self.recache()
        return self._path

    @property
    def _is_view(self):
        """Return boolean indicating if self is view of another array """
        return self._data.is_view

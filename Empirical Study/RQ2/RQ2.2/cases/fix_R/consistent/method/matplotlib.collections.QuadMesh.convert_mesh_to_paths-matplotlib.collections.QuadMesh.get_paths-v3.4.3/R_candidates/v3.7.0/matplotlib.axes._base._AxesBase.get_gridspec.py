    def get_gridspec(self):
        """Return the `.GridSpec` associated with the subplot, or None."""
        return self._subplotspec.get_gridspec() if self._subplotspec else None

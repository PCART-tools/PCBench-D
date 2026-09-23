    @property
    def _selection_list(self):
        if not isinstance(self._selection, (list, tuple, Series, np.ndarray)):
            return [self._selection]
        return self._selection

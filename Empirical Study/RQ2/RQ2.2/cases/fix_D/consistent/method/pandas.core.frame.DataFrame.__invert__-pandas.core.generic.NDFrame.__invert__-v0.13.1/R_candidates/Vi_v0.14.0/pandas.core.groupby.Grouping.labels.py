    @property
    def labels(self):
        if self._labels is None:
            self._make_labels()
        return self._labels

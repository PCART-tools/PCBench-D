    def _entry_from_axes(self, e):
        return next(((ind, a) for ind, a in self._elements if a == e), None)

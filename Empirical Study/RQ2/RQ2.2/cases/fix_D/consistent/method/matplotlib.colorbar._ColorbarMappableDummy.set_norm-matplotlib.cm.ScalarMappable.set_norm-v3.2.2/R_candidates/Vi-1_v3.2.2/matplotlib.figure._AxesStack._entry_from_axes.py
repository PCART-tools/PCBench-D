    def _entry_from_axes(self, e):
        ind, k = {a: (ind, k) for k, (ind, a) in self._elements}[e]
        return (k, (ind, e))

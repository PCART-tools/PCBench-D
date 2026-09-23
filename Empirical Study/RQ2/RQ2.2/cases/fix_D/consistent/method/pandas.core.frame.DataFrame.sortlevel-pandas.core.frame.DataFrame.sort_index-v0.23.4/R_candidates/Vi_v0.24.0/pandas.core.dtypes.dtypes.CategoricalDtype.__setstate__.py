    def __setstate__(self, state):
        self._categories = state.pop('categories', None)
        self._ordered = state.pop('ordered', False)

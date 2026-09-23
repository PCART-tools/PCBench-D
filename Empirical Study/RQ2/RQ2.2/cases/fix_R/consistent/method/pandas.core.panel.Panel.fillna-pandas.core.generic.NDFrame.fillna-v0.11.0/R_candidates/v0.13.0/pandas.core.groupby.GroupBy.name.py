    @property
    def name(self):
        if self._selection is None:
            return None  # 'result'
        else:
            return self._selection

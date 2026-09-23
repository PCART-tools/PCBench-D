    @codes.setter
    def codes(self, codes):
        if self._readonly:
            raise AttributeError("Can't set codes on a readonly Path")
        self._codes = codes
        self._update_values()

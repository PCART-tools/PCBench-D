    def _get_numeric_data(self):
        return self._constructor(
            self._data.get_numeric_data()).__finalize__(self)

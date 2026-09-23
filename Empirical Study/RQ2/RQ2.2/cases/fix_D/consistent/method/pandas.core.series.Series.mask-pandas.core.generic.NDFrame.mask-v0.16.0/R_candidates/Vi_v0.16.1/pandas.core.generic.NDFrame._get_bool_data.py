    def _get_bool_data(self):
        return self._constructor(self._data.get_bool_data()).__finalize__(self)

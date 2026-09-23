    @property
    def _dt_year(self):
        return type(self)(pc.year(self._data))

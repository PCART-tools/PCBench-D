    @property
    def _dt_is_leap_year(self):
        return type(self)(pc.is_leap_year(self._data))

    @property
    def _dt_microsecond(self):
        return type(self)(pc.microsecond(self._data))

    @property
    def _dt_nanosecond(self):
        return type(self)(pc.nanosecond(self._data))

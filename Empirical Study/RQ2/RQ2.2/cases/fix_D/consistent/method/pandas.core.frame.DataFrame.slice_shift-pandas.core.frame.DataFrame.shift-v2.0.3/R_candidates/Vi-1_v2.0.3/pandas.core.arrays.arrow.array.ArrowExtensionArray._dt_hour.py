    @property
    def _dt_hour(self):
        return type(self)(pc.hour(self._data))

    @property
    def _dt_second(self):
        return type(self)(pc.second(self._data))

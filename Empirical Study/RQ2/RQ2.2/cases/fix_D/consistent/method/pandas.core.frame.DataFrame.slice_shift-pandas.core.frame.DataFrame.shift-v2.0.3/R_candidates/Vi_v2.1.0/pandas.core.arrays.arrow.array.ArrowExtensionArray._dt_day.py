    @property
    def _dt_day(self):
        return type(self)(pc.day(self._pa_array))

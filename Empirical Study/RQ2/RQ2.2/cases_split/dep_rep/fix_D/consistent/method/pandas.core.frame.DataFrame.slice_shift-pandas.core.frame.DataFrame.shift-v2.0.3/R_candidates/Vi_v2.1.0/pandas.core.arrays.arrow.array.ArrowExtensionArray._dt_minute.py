    @property
    def _dt_minute(self):
        return type(self)(pc.minute(self._pa_array))

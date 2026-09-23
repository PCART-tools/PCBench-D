    @property
    def _dt_month(self):
        return type(self)(pc.month(self._pa_array))

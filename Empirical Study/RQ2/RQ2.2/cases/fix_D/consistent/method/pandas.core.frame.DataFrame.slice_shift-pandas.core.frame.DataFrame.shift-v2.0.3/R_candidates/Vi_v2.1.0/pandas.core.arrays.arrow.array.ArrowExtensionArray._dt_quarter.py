    @property
    def _dt_quarter(self):
        return type(self)(pc.quarter(self._pa_array))

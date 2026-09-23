    @property
    def _dt_day_of_year(self):
        return type(self)(pc.day_of_year(self._pa_array))

    @property
    def _dt_day_of_week(self):
        return type(self)(pc.day_of_week(self._pa_array))

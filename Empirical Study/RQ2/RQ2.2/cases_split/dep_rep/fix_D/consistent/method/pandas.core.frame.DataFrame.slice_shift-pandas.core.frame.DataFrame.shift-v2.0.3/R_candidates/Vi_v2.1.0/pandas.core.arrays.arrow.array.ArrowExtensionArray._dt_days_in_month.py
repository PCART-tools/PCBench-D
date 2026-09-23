    @property
    def _dt_days_in_month(self):
        result = pc.days_between(
            pc.floor_temporal(self._pa_array, unit="month"),
            pc.ceil_temporal(self._pa_array, unit="month"),
        )
        return type(self)(result)

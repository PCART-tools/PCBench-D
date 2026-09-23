    @property
    def _dt_is_month_end(self):
        result = pc.equal(
            pc.days_between(
                pc.floor_temporal(self._pa_array, unit="day"),
                pc.ceil_temporal(self._pa_array, unit="month"),
            ),
            1,
        )
        return type(self)(result)

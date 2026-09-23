    @property
    def _dt_is_quarter_end(self):
        result = pc.equal(
            pc.days_between(
                pc.floor_temporal(self._pa_array, unit="day"),
                pc.ceil_temporal(self._pa_array, unit="quarter"),
            ),
            1,
        )
        return type(self)(result)

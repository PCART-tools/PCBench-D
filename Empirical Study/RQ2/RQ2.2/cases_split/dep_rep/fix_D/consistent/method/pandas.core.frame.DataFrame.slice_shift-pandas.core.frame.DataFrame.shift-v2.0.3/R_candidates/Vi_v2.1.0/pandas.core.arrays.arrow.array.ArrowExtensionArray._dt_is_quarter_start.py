    @property
    def _dt_is_quarter_start(self):
        result = pc.equal(
            pc.floor_temporal(self._pa_array, unit="quarter"),
            pc.floor_temporal(self._pa_array, unit="day"),
        )
        return type(self)(result)

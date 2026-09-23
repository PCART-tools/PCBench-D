    @property
    def _dt_is_month_start(self):
        return type(self)(pc.equal(pc.day(self._pa_array), 1))

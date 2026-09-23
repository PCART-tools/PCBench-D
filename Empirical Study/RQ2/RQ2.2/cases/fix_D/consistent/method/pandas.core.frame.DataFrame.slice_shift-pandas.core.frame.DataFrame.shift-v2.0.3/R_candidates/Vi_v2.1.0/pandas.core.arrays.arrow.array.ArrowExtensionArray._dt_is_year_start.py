    @property
    def _dt_is_year_start(self):
        return type(self)(
            pc.and_(
                pc.equal(pc.month(self._pa_array), 1),
                pc.equal(pc.day(self._pa_array), 1),
            )
        )

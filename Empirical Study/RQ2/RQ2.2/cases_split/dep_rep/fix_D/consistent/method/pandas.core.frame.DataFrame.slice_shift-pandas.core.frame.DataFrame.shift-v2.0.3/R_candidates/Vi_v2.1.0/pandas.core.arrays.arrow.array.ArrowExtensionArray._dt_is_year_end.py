    @property
    def _dt_is_year_end(self):
        return type(self)(
            pc.and_(
                pc.equal(pc.month(self._pa_array), 12),
                pc.equal(pc.day(self._pa_array), 31),
            )
        )

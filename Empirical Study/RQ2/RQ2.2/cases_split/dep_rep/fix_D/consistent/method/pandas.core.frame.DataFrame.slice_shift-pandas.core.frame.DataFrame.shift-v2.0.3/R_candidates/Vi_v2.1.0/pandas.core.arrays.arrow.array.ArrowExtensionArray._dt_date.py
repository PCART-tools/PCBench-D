    @property
    def _dt_date(self):
        return type(self)(self._pa_array.cast(pa.date32()))

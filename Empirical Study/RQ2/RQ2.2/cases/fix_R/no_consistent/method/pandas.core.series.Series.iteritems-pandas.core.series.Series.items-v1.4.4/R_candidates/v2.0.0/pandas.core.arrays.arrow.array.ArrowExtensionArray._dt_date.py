    @property
    def _dt_date(self):
        return type(self)(self._data.cast(pa.date32()))

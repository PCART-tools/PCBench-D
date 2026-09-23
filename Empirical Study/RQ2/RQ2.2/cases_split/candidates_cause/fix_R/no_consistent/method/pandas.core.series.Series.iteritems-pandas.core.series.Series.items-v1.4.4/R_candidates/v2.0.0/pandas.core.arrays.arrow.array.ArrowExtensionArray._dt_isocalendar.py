    def _dt_isocalendar(self):
        return type(self)(pc.iso_calendar(self._data))

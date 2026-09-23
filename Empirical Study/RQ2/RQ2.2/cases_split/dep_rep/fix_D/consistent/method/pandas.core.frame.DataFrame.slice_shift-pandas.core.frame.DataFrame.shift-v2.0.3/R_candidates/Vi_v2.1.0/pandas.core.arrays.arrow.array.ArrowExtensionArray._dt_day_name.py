    def _dt_day_name(self, locale: str | None = None):
        if locale is None:
            locale = "C"
        return type(self)(pc.strftime(self._pa_array, format="%A", locale=locale))

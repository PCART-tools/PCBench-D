    def _dt_strftime(self, format: str):
        return type(self)(pc.strftime(self._data, format=format))

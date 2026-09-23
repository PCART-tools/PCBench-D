    def _str_istitle(self):
        result = pc.utf8_is_title(self._data)
        return BooleanDtype().__from_arrow__(result)

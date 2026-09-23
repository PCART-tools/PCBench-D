    def _str_isspace(self):
        if pa_version_under2p0:
            fallback_performancewarning(version="2")
            return super()._str_isspace()

        result = pc.utf8_is_space(self._data)
        return BooleanDtype().__from_arrow__(result)

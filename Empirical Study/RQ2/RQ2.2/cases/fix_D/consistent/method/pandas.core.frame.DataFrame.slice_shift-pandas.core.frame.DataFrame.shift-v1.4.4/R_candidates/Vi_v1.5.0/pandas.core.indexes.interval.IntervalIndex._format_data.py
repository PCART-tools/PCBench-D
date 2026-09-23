    def _format_data(self, name=None) -> str:
        # TODO: integrate with categorical and make generic
        # name argument is unused here; just for compat with base / categorical
        return self._data._format_data() + "," + self._format_space()

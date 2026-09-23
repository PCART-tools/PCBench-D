    @cbook.deprecated("3.3")
    @property
    def serif(self):
        return self._fonts.get("serif", ('cmr', ''))

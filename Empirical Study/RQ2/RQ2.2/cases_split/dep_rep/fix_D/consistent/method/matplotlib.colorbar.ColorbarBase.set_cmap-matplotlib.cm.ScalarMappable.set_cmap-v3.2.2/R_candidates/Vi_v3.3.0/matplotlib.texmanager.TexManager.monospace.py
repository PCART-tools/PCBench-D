    @cbook.deprecated("3.3")
    @property
    def monospace(self):
        return self._fonts.get("monospace", ('cmtt', ''))

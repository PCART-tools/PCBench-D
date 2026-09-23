    @cbook.deprecated("3.3")
    @property
    def sans_serif(self):
        return self._fonts.get("sans-serif", ('cmss', ''))

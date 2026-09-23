    def _expand(self, xmargin: int, ymargin: int | None = None) -> Image:
        if ymargin is None:
            ymargin = xmargin
        self.load()
        return self._new(self.im.expand(xmargin, ymargin))

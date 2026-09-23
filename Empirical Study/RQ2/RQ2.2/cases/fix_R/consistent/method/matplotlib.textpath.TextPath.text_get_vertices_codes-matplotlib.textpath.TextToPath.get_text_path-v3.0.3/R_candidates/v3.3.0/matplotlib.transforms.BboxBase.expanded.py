    def expanded(self, sw, sh):
        """
        Construct a `Bbox` by expanding this one around its center by the
        factors *sw* and *sh*.
        """
        width = self.width
        height = self.height
        deltaw = (sw * width - width) / 2.0
        deltah = (sh * height - height) / 2.0
        a = np.array([[-deltaw, -deltah], [deltaw, deltah]])
        return Bbox(self._points + a)

    def expanded(self, sw, sh):
        """
        Return a new :class:`Bbox` which is this :class:`Bbox`
        expanded around its center by the given factors *sw* and
        *sh*.
        """
        width = self.width
        height = self.height
        deltaw = (sw * width - width) / 2.0
        deltah = (sh * height - height) / 2.0
        a = np.array([[-deltaw, -deltah], [deltaw, deltah]])
        return Bbox(self._points + a)

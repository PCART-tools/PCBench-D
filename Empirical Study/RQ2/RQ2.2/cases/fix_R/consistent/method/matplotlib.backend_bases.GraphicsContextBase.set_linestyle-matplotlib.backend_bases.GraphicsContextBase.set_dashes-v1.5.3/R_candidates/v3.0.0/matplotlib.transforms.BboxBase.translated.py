    def translated(self, tx, ty):
        """
        Return a copy of the :class:`Bbox`, statically translated by
        *tx* and *ty*.
        """
        return Bbox(self._points + (tx, ty))

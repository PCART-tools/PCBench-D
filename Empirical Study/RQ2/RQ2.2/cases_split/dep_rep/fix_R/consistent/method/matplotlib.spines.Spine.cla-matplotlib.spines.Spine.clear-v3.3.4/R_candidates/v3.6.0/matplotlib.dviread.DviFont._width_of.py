    def _width_of(self, char):
        """Width of char in dvi units."""
        width = self._tfm.width.get(char, None)
        if width is not None:
            return _mul2012(width, self._scale)
        _log.debug('No width for char %d in font %s.', char, self.texname)
        return 0

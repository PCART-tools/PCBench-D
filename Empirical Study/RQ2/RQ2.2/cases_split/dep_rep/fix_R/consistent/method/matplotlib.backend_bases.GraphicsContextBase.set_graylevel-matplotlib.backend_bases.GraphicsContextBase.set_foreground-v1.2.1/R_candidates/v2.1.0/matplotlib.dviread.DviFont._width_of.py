    def _width_of(self, char):
        """
        Width of char in dvi units. For internal use by dviread.py.
        """

        width = self._tfm.width.get(char, None)
        if width is not None:
            return _mul2012(width, self._scale)

        matplotlib.verbose.report(
            'No width for char %d in font %s' % (char, self.texname),
            'debug')
        return 0

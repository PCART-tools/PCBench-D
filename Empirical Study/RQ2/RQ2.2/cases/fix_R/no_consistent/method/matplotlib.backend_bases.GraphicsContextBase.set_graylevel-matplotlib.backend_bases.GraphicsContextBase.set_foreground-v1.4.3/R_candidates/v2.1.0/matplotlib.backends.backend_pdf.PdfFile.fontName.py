    def fontName(self, fontprop):
        """
        Select a font based on fontprop and return a name suitable for
        Op.selectfont. If fontprop is a string, it will be interpreted
        as the filename of the font.
        """

        if isinstance(fontprop, six.string_types):
            filename = fontprop
        elif rcParams['pdf.use14corefonts']:
            filename = findfont(
                fontprop, fontext='afm', directory=self._core14fontdir)
            if filename is None:
                filename = findfont(
                    "Helvetica", fontext='afm', directory=self._core14fontdir)
        else:
            filename = findfont(fontprop)

        Fx = self.fontNames.get(filename)
        if Fx is None:
            Fx = Name('F%d' % self.nextFont)
            self.fontNames[filename] = Fx
            self.nextFont += 1
            matplotlib.verbose.report(
                'Assigning font %s = %r' % (Fx, filename),
                'debug')

        return Fx

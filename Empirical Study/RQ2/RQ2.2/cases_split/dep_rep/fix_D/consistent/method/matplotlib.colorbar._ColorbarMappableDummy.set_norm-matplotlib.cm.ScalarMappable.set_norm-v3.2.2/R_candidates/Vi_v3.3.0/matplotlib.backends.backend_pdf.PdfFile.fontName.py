    def fontName(self, fontprop):
        """
        Select a font based on fontprop and return a name suitable for
        Op.selectfont. If fontprop is a string, it will be interpreted
        as the filename of the font.
        """

        if isinstance(fontprop, str):
            filename = fontprop
        elif mpl.rcParams['pdf.use14corefonts']:
            filename = findfont(
                fontprop, fontext='afm', directory=RendererPdf._afm_font_dir)
        else:
            filename = findfont(fontprop)

        Fx = self.fontNames.get(filename)
        if Fx is None:
            Fx = next(self._internal_font_seq)
            self.fontNames[filename] = Fx
            _log.debug('Assigning font %s = %r', Fx, filename)

        return Fx

    def fontName(self, fontprop):
        """
        Select a font based on fontprop and return a name suitable for
        Op.selectfont. If fontprop is a string, it will be interpreted
        as the filename of the font.
        """

        if isinstance(fontprop, str):
            filenames = [fontprop]
        elif mpl.rcParams['pdf.use14corefonts']:
            filenames = _fontManager._find_fonts_by_props(
                fontprop, fontext='afm', directory=RendererPdf._afm_font_dir
            )
        else:
            filenames = _fontManager._find_fonts_by_props(fontprop)
        first_Fx = None
        for fname in filenames:
            Fx = self.fontNames.get(fname)
            if not first_Fx:
                first_Fx = Fx
            if Fx is None:
                Fx = next(self._internal_font_seq)
                self.fontNames[fname] = Fx
                _log.debug('Assigning font %s = %r', Fx, fname)
                if not first_Fx:
                    first_Fx = Fx

        # find_fontsprop's first value always adheres to
        # findfont's value, so technically no behaviour change
        return first_Fx

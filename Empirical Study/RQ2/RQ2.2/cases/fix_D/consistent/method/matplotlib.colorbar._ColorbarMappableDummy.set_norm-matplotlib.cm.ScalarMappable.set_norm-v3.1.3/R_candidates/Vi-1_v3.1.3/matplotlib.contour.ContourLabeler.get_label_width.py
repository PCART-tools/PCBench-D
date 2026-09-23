    def get_label_width(self, lev, fmt, fsize):
        """
        Return the width of the label in points.
        """
        if not isinstance(lev, str):
            lev = self.get_text(lev, fmt)

        lev, ismath = text.Text()._preprocess_math(lev)
        if ismath == 'TeX':
            if not hasattr(self, '_TeX_manager'):
                self._TeX_manager = texmanager.TexManager()
            lw, _, _ = self._TeX_manager.get_text_width_height_descent(lev,
                                                                       fsize)
        elif ismath:
            if not hasattr(self, '_mathtext_parser'):
                self._mathtext_parser = mathtext.MathTextParser('bitmap')
            img, _ = self._mathtext_parser.parse(lev, dpi=72,
                                                 prop=self.labelFontProps)
            lw = img.get_width()  # at dpi=72, the units are PostScript points
        else:
            # width is much less than "font size"
            lw = (len(lev)) * fsize * 0.6

        return lw

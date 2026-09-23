    @property
    def texFontMap(self):
        # lazy-load texFontMap, it takes a while to parse
        # and usetex is a relatively rare use case
        if self._texFontMap is None:
            self._texFontMap = dviread.PsfontsMap(
                dviread.find_tex_file('pdftex.map'))

        return self._texFontMap

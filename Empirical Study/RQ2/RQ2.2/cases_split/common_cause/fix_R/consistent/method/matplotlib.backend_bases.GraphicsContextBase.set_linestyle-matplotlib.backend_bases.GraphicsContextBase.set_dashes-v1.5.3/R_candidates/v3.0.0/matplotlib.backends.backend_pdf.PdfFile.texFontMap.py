    @property
    @cbook.deprecated("3.0")
    def texFontMap(self):
        # lazy-load texFontMap, it takes a while to parse
        # and usetex is a relatively rare use case
        return dviread.PsfontsMap(dviread.find_tex_file('pdftex.map'))

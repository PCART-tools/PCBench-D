    @property
    @cbook.deprecated("3.0")
    def tex_font_map(self):
        return dviread.PsfontsMap(dviread.find_tex_file('pdftex.map'))

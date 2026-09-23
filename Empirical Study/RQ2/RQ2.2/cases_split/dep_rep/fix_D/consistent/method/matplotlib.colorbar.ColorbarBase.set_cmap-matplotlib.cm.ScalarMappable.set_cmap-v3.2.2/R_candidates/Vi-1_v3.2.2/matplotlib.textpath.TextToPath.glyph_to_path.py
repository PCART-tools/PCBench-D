    @cbook.deprecated(
        "3.1",
        alternative="font.get_path() and manual translation of the vertices")
    def glyph_to_path(self, font, currx=0.):
        """Convert the *font*'s current glyph to a (vertices, codes) pair."""
        verts, codes = font.get_path()
        if currx != 0.0:
            verts[:, 0] += currx
        return verts, codes

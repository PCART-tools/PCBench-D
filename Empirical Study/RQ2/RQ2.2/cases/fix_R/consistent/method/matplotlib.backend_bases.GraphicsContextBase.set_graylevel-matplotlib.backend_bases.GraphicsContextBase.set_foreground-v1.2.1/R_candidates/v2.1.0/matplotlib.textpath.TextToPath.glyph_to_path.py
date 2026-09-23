    def glyph_to_path(self, font, currx=0.):
        """
        convert the ft2font glyph to vertices and codes.
        """
        verts, codes = font.get_path()
        if currx != 0.0:
            verts[:, 0] += currx
        return verts, codes

    @cbook._delete_parameter("3.1", "usetex")
    def get_text_path(self, prop, s, ismath=False, usetex=False):
        """
        Convert text *s* to path (a tuple of vertices and codes for
        matplotlib.path.Path).

        Parameters
        ----------
        prop : `matplotlib.font_manager.FontProperties` instance
            The font properties for the text.

        s : str
            The text to be converted.

        ismath : {False, True, "TeX"}
            If True, use mathtext parser.  If "TeX", use tex for renderering.

        usetex : bool, optional
            If set, forces *ismath* to True.  This parameter is deprecated.

        Returns
        -------
        verts, codes : tuple of lists
            *verts*  is a list of numpy arrays containing the x and y
            coordinates of the vertices. *codes* is a list of path codes.

        Examples
        --------
        Create a list of vertices and codes from a text, and create a `Path`
        from those::

            from matplotlib.path import Path
            from matplotlib.textpath import TextToPath
            from matplotlib.font_manager import FontProperties

            fp = FontProperties(family="Humor Sans", style="italic")
            verts, codes = TextToPath().get_text_path(fp, "ABC")
            path = Path(verts, codes, closed=False)

        Also see `TextPath` for a more direct way to create a path from a text.
        """
        if usetex:
            ismath = "TeX"
        if ismath == "TeX":
            glyph_info, glyph_map, rects = self.get_glyphs_tex(prop, s)
        elif not ismath:
            font = self._get_font(prop)
            glyph_info, glyph_map, rects = self.get_glyphs_with_font(font, s)
        else:
            glyph_info, glyph_map, rects = self.get_glyphs_mathtext(prop, s)

        verts, codes = [], []

        for glyph_id, xposition, yposition, scale in glyph_info:
            verts1, codes1 = glyph_map[glyph_id]
            if len(verts1):
                verts1 = np.array(verts1) * scale + [xposition, yposition]
                verts.extend(verts1)
                codes.extend(codes1)

        for verts1, codes1 in rects:
            verts.extend(verts1)
            codes.extend(codes1)

        return verts, codes

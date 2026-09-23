    def text_get_vertices_codes(self, prop, s, usetex):
        """
        convert the string *s* to vertices and codes using the
        provided font property *prop*. Mostly copied from
        backend_svg.py.
        """

        if usetex:
            verts, codes = text_to_path.get_text_path(prop, s, usetex=True)
        else:
            clean_line, ismath = self.is_math_text(s)
            verts, codes = text_to_path.get_text_path(prop, clean_line,
                                                      ismath=ismath)

        return verts, codes

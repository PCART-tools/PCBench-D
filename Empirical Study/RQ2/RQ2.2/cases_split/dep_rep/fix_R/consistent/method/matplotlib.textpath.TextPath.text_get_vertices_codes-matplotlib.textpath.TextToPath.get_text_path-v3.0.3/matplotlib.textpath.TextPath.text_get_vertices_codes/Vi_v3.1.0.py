    @cbook.deprecated("3.1", alternative="TextPath")
    def text_get_vertices_codes(self, prop, s, usetex):
        """
        Convert string *s* to a (vertices, codes) pair using font property
        *prop*.
        """
        # Mostly copied from backend_svg.py.
        if usetex:
            return text_to_path.get_text_path(prop, s, usetex=True)
        else:
            clean_line, ismath = self.is_math_text(s)
            return text_to_path.get_text_path(prop, clean_line, ismath=ismath)

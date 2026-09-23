    def _get_xobject_glyph_name(self, filename, glyph_name):
        Fx = self.fontName(filename)
        return "-".join([
            Fx.name.decode(),
            os.path.splitext(os.path.basename(filename))[0],
            glyph_name])

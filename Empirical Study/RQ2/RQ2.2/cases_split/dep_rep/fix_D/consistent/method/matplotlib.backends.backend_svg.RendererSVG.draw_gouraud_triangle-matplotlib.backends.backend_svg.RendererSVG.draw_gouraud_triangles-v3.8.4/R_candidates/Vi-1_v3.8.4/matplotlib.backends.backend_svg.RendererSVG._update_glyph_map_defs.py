    def _update_glyph_map_defs(self, glyph_map_new):
        """
        Emit definitions for not-yet-defined glyphs, and record them as having
        been defined.
        """
        writer = self.writer
        if glyph_map_new:
            writer.start('defs')
            for char_id, (vertices, codes) in glyph_map_new.items():
                char_id = self._adjust_char_id(char_id)
                # x64 to go back to FreeType's internal (integral) units.
                path_data = self._convert_path(
                    Path(vertices * 64, codes), simplify=False)
                writer.element(
                    'path', id=char_id, d=path_data,
                    transform=_generate_transform([('scale', (1 / 64,))]))
            writer.end('defs')
            self._glyph_map.update(glyph_map_new)

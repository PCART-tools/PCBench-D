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
                path_data = self._convert_path(
                    Path(vertices, codes), simplify=False)
                writer.element('path', id=char_id, d=path_data)
            writer.end('defs')
            self._glyph_map.update(glyph_map_new)

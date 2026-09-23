    def _get_glyph(self, fontname: str, font_class: str,
                   sym: str) -> tuple[FT2Font, int, bool]:
        raise NotImplementedError

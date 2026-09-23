    def render_glyph(self, output: Output, ox: float, oy: float, font: str,
                     font_class: str, sym: str, fontsize: float, dpi: float) -> None:
        """
        At position (*ox*, *oy*), draw the glyph specified by the remaining
        parameters (see `get_metrics` for their detailed description).
        """
        info = self._get_info(font, font_class, sym, fontsize, dpi)
        output.glyphs.append((ox, oy, info))

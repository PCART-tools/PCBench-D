    def _get_offset(self, font: FT2Font, glyph: Glyph, fontsize: float,
                    dpi: float) -> float:
        if font.postscript_name == 'Cmex10':
            return (glyph.height / 64 / 2) + (fontsize/3 * dpi/72)
        return 0.

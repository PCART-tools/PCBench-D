@_api.deprecated("3.4", alternative="MathtextBackendPath")
class MathtextBackendPdf(MathtextBackend):
    """Store information to write a mathtext rendering to the PDF backend."""

    _PDFResult = namedtuple(
        "_PDFResult", "width height depth glyphs rects used_characters")

    def __init__(self):
        super().__init__()
        self.glyphs = []
        self.rects = []

    def render_glyph(self, ox, oy, info):
        filename = info.font.fname
        oy = self.height - oy + info.offset
        self.glyphs.append(
            (ox, oy, filename, info.fontsize,
             info.num, info.symbol_name))

    def render_rect_filled(self, x1, y1, x2, y2):
        self.rects.append((x1, self.height - y2, x2 - x1, y2 - y1))

    def get_results(self, box, used_characters):
        _mathtext.ship(0, 0, box)
        return self._PDFResult(self.width,
                               self.height + self.depth,
                               self.depth,
                               self.glyphs,
                               self.rects,
                               used_characters)

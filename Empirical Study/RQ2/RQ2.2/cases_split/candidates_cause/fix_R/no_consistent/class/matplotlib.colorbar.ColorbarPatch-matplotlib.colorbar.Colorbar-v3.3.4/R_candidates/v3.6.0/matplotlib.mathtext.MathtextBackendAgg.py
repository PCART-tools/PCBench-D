@_api.deprecated("3.6")
class MathtextBackendAgg(MathtextBackend):
    """
    Render glyphs and rectangles to an FTImage buffer, which is later
    transferred to the Agg image by the Agg backend.
    """
    def __init__(self):
        self.ox = 0
        self.oy = 0
        self.image = None
        self.mode = 'bbox'
        self.bbox = [0, 0, 0, 0]
        super().__init__()

    def _update_bbox(self, x1, y1, x2, y2):
        self.bbox = [min(self.bbox[0], x1),
                     min(self.bbox[1], y1),
                     max(self.bbox[2], x2),
                     max(self.bbox[3], y2)]

    def set_canvas_size(self, w, h, d):
        super().set_canvas_size(w, h, d)
        if self.mode != 'bbox':
            self.image = FT2Image(np.ceil(w), np.ceil(h + max(d, 0)))

    def render_glyph(self, ox, oy, info):
        if self.mode == 'bbox':
            self._update_bbox(ox + info.metrics.xmin,
                              oy - info.metrics.ymax,
                              ox + info.metrics.xmax,
                              oy - info.metrics.ymin)
        else:
            info.font.draw_glyph_to_bitmap(
                self.image, ox, oy - info.metrics.iceberg, info.glyph,
                antialiased=mpl.rcParams['text.antialiased'])

    def render_rect_filled(self, x1, y1, x2, y2):
        if self.mode == 'bbox':
            self._update_bbox(x1, y1, x2, y2)
        else:
            height = max(int(y2 - y1) - 1, 0)
            if height == 0:
                center = (y2 + y1) / 2.0
                y = int(center - (height + 1) / 2.0)
            else:
                y = int(y1)
            self.image.draw_rect_filled(int(x1), y, np.ceil(x2), y + height)

    def get_results(self, box):
        self.image = None
        self.mode = 'render'
        return _mathtext.ship(box).to_raster()

    def get_hinting_type(self):
        from matplotlib.backends import backend_agg
        return backend_agg.get_hinting_flag()

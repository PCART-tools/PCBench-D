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

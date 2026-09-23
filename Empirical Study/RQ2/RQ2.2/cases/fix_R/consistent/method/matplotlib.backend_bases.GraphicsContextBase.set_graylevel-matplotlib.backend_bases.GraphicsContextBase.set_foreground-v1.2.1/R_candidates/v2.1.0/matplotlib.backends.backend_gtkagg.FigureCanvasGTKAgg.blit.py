    def blit(self, bbox=None):
        if DEBUG: print('FigureCanvasGTKAgg.blit', self._pixmap)
        agg_to_gtk_drawable(self._pixmap, self.renderer._renderer, bbox)

        x, y, w, h = self.allocation

        self.window.draw_drawable (self.style.fg_gc[self.state], self._pixmap,
                                   0, 0, 0, 0, w, h)
        if DEBUG: print('FigureCanvasGTKAgg.done')

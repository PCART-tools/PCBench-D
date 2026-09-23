    def set_linewidth(self, w):
        GraphicsContextBase.set_linewidth(self, w)
        if w == 0:
            self.gdkGC.line_width = 0
        else:
            pixels = self.renderer.points_to_pixels(w)
            self.gdkGC.line_width = max(1, int(np.round(pixels)))

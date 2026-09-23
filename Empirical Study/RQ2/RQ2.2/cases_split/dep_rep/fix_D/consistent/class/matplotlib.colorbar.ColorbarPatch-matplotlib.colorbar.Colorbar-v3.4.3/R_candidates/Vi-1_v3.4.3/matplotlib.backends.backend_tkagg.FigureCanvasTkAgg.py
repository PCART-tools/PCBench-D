class FigureCanvasTkAgg(FigureCanvasAgg, FigureCanvasTk):
    def draw(self):
        super().draw()
        self.blit()

    def blit(self, bbox=None):
        _backend_tk.blit(self._tkphoto, self.renderer.buffer_rgba(),
                         (0, 1, 2, 3), bbox=bbox)

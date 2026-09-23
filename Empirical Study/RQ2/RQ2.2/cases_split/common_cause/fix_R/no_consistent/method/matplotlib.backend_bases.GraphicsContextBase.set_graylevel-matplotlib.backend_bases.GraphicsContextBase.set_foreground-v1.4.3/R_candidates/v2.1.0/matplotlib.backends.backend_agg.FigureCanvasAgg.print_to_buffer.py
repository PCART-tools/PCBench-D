    def print_to_buffer(self):
        FigureCanvasAgg.draw(self)
        renderer = self.get_renderer()
        original_dpi = renderer.dpi
        renderer.dpi = self.figure.dpi
        try:
            result = (renderer._renderer.buffer_rgba(),
                      (int(renderer.width), int(renderer.height)))
        finally:
            renderer.dpi = original_dpi
        return result

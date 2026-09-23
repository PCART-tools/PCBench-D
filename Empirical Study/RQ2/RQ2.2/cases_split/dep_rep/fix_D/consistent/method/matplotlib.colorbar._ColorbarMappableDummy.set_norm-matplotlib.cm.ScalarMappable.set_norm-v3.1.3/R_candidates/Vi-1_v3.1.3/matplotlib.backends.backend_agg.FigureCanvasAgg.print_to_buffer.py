    def print_to_buffer(self):
        FigureCanvasAgg.draw(self)
        renderer = self.get_renderer()
        with cbook._setattr_cm(renderer, dpi=self.figure.dpi):
            return (renderer._renderer.buffer_rgba(),
                    (int(renderer.width), int(renderer.height)))

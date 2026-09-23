    def resize(self, width, height):
        dpi = self.figure.dpi
        width /= dpi
        height /= dpi
        self.figure.set_size_inches(width * self._dpi_ratio,
                                    height * self._dpi_ratio,
                                    forward=False)
        FigureCanvasBase.resize_event(self)
        self.draw_idle()

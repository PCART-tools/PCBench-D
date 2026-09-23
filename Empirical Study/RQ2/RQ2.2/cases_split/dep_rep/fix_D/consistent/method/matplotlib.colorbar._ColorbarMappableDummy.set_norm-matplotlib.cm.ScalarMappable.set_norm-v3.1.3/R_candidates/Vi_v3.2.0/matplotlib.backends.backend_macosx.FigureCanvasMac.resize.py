    def resize(self, width, height):
        dpi = self.figure.dpi
        width /= dpi
        height /= dpi
        self.figure.set_size_inches(width * self._device_scale,
                                    height * self._device_scale,
                                    forward=False)
        FigureCanvasBase.resize_event(self)
        self.draw_idle()

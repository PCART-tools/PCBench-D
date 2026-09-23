    def get_width_height(self):
        w, h = FigureCanvasBase.get_width_height(self)
        return int(w / self._dpi_ratio), int(h / self._dpi_ratio)

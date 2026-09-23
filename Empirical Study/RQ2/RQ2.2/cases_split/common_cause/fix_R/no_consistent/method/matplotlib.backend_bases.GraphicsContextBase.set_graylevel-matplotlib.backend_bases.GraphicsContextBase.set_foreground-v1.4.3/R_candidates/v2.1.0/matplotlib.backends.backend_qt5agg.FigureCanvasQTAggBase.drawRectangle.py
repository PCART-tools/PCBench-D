    def drawRectangle(self, rect):
        if rect is not None:
            self._drawRect = [pt / self._dpi_ratio for pt in rect]
        else:
            self._drawRect = None
        self.update()

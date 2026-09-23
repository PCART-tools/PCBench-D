    def sizeHint(self):
        size = super().sizeHint()
        if is_pyqt5() and self.canvas._dpi_ratio > 1:
            # For some reason, self.setMinimumHeight doesn't seem to carry over
            # to the actual sizeHint, so override it instead in order to make
            # the aesthetic adjustments noted above.
            size.setHeight(max(48, size.height()))
        return size

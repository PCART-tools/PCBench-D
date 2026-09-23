    def handle_set_dpi_ratio(self, event):
        dpi_ratio = event.get('dpi_ratio', 1)
        if dpi_ratio != self._dpi_ratio:
            # We don't want to scale up the figure dpi more than once.
            if not hasattr(self.figure, '_original_dpi'):
                self.figure._original_dpi = self.figure.dpi
            self.figure.dpi = dpi_ratio * self.figure._original_dpi
            self._dpi_ratio = dpi_ratio
            self._force_full = True
            self.draw_idle()

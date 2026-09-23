    def _update_figure_dpi(self):
        dpi = self._dpi_ratio * self.figure._original_dpi
        self.figure._set_dpi(dpi, forward=False)

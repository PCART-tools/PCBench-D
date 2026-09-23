    def _set_dpi(self, dpi, forward=True):
        """
        The forward kwarg is passed on to set_size_inches
        """
        self._dpi = dpi
        self.dpi_scale_trans.clear().scale(dpi, dpi)
        w, h = self.get_size_inches()
        self.set_size_inches(w, h, forward=forward)
        self.callbacks.process('dpi_changed', self)

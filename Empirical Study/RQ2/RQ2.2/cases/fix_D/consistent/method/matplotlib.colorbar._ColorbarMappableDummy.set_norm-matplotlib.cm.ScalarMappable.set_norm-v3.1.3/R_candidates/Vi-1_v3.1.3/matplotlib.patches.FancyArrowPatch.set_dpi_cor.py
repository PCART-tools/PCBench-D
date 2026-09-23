    def set_dpi_cor(self, dpi_cor):
        """
        dpi_cor is currently used for linewidth-related things and
        shrink factor. Mutation scale is affected by this.

        Parameters
        ----------
        dpi_cor : scalar
        """
        self._dpi_cor = dpi_cor
        self.stale = True

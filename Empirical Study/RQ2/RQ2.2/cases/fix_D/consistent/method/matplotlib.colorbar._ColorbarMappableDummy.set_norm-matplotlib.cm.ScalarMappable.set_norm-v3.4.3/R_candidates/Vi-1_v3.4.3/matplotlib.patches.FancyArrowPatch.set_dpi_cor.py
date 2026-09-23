    @_api.deprecated("3.4")
    def set_dpi_cor(self, dpi_cor):
        """
        dpi_cor is currently used for linewidth-related things and
        shrink factor. Mutation scale is affected by this.

        Parameters
        ----------
        dpi_cor : float
        """
        self._dpi_cor = dpi_cor
        self.stale = True

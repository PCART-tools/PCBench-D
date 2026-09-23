    @_api.deprecated("3.4")
    def get_dpi_cor(self):
        """
        dpi_cor is currently used for linewidth-related things and
        shrink factor. Mutation scale is affected by this.

        Returns
        -------
        scalar
        """
        return self._dpi_cor

    def set_norm(self, norm):
        """Set the normalization instance.

        Parameters
        ----------
        norm : `.Normalize`

        Notes
        -----
        If there are any colorbars using the mappable for this norm, setting
        the norm of the mappable will reset the norm, locator, and formatters
        on the colorbar to default.

        """
        if norm is None:
            norm = colors.Normalize()
        self.norm = norm
        self.changed()

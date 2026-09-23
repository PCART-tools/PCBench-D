    def set_norm(self, norm):
        """
        Set the normalization instance.

        Parameters
        ----------
        norm : `.Normalize` or None

        Notes
        -----
        If there are any colorbars using the mappable for this norm, setting
        the norm of the mappable will reset the norm, locator, and formatters
        on the colorbar to default.
        """
        cbook._check_isinstance((colors.Normalize, None), norm=norm)
        in_init = self.norm is None
        if norm is None:
            norm = colors.Normalize()
        self.norm = norm
        if not in_init:
            self.changed()  # Things are not set up properly yet.

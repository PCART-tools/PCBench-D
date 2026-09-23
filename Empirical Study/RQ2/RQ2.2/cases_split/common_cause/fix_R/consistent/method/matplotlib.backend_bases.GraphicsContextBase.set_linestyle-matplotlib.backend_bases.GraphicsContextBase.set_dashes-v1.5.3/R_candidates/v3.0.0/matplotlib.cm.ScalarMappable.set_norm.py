    def set_norm(self, norm):
        """Set the normalization instance.

        Parameters
        ----------
        norm : `.Normalize`
        """
        if norm is None:
            norm = colors.Normalize()
        self.norm = norm
        self.changed()

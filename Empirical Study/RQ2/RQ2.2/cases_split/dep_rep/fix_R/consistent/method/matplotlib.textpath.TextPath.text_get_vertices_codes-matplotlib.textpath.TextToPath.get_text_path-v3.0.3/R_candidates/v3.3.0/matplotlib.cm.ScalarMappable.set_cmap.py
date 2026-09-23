    def set_cmap(self, cmap):
        """
        Set the colormap for luminance data.

        Parameters
        ----------
        cmap : `.Colormap` or str or None
        """
        in_init = self.cmap is None
        cmap = get_cmap(cmap)
        self.cmap = cmap
        if not in_init:
            self.changed()  # Things are not set up properly yet.

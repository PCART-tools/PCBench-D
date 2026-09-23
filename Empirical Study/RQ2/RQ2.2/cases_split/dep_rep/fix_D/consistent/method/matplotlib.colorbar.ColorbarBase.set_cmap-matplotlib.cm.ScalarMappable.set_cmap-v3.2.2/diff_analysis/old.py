    def set_cmap(self, cmap):
        """
        set the colormap for luminance data

        Parameters
        ----------
        cmap : colormap or registered colormap name
        """
        cmap = get_cmap(cmap)
        self.cmap = cmap
        self.changed()

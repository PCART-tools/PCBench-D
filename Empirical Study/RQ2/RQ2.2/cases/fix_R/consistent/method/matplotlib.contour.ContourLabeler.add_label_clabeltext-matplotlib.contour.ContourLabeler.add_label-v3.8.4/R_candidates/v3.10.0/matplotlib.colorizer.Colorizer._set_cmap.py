    def _set_cmap(self, cmap):
        """
        Set the colormap for luminance data.

        Parameters
        ----------
        cmap : `.Colormap` or str or None
        """
        # bury import to avoid circular imports
        from matplotlib import cm
        in_init = self._cmap is None
        self._cmap = cm._ensure_cmap(cmap)
        if not in_init:
            self.changed()  # Things are not set up properly yet.

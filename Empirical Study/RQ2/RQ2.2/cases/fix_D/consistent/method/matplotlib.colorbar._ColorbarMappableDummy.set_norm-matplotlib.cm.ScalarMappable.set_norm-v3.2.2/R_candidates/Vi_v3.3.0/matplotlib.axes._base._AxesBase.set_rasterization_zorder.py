    def set_rasterization_zorder(self, z):
        """
        Parameters
        ----------
        z : float or None
            zorder below which artists are rasterized.  ``None`` means that
            artists do not get rasterized based on zorder.
        """
        self._rasterization_zorder = z
        self.stale = True

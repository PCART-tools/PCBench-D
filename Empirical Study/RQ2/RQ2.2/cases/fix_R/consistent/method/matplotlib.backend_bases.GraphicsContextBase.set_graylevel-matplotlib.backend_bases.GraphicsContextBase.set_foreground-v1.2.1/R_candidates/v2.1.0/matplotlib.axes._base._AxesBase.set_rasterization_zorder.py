    def set_rasterization_zorder(self, z):
        """
        Set zorder value below which artists will be rasterized.  Set
        to `None` to disable rasterizing of artists below a particular
        zorder.
        """
        self._rasterization_zorder = z
        self.stale = True

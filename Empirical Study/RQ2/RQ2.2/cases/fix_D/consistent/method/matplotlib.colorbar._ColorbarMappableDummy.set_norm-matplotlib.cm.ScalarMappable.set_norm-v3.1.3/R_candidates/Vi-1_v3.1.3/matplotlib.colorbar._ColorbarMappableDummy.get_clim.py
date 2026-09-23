    @cbook.deprecated("3.1", alternative="ScalarMappable.get_clim")
    def get_clim(self):
        """
        return the min, max of the color limits for image scaling
        """
        return self.norm.vmin, self.norm.vmax

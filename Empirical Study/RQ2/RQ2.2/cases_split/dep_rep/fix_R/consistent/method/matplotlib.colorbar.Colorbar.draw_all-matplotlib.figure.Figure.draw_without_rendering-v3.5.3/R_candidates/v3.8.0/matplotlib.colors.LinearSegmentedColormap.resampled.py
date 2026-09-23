    def resampled(self, lutsize):
        """Return a new colormap with *lutsize* entries."""
        new_cmap = LinearSegmentedColormap(self.name, self._segmentdata,
                                           lutsize)
        new_cmap._rgba_over = self._rgba_over
        new_cmap._rgba_under = self._rgba_under
        new_cmap._rgba_bad = self._rgba_bad
        return new_cmap

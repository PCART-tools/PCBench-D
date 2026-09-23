    def _resample(self, lutsize):
        """
        Return a new color map with *lutsize* entries.
        """
        return LinearSegmentedColormap(self.name, self._segmentdata, lutsize)

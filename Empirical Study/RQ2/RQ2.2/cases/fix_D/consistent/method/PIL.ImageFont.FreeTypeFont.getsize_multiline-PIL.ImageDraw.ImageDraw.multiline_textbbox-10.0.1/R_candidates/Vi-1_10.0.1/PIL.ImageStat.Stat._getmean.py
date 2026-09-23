    def _getmean(self):
        """Get average pixel level for each layer"""

        v = []
        for i in self.bands:
            v.append(self.sum[i] / self.count[i])
        return v

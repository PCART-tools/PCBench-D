    def _getvar(self):
        """Get variance for each layer"""
        return [
            (self.sum2[i] - (self.sum[i] ** 2.0) / self.count[i]) / self.count[i]
            for i in self.bands
        ]

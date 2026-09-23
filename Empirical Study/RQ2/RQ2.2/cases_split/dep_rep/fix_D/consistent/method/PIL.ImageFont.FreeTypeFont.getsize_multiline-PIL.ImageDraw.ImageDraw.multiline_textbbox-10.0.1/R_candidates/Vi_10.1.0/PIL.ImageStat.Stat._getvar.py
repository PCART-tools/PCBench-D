    def _getvar(self):
        """Get variance for each layer"""

        v = []
        for i in self.bands:
            n = self.count[i]
            v.append((self.sum2[i] - (self.sum[i] ** 2.0) / n) / n)
        return v

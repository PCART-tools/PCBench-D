    def _getrms(self):
        """Get RMS for each layer"""

        v = []
        for i in self.bands:
            v.append(math.sqrt(self.sum2[i] / self.count[i]))
        return v

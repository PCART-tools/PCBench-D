    def _getstddev(self):
        """Get standard deviation for each layer"""

        v = []
        for i in self.bands:
            v.append(math.sqrt(self.var[i]))
        return v

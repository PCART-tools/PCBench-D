    def _getstddev(self):
        """Get standard deviation for each layer"""
        return [math.sqrt(self.var[i]) for i in self.bands]

    def _slice(self, slicer):
        """ return a slice of my values (but densify first) """
        return self.get_values()[slicer]

    def _slice(self, slicer):
        """ return a slice of my values """

        # slice the category
        # return same dims as we currently have
        return self.values._slice(slicer)

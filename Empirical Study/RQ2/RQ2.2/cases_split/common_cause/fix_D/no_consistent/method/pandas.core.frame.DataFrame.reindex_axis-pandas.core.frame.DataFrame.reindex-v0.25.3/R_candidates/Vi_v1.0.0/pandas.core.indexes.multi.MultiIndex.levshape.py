    @property
    def levshape(self):
        """
        A tuple with the length of each level.
        """
        return tuple(len(x) for x in self.levels)

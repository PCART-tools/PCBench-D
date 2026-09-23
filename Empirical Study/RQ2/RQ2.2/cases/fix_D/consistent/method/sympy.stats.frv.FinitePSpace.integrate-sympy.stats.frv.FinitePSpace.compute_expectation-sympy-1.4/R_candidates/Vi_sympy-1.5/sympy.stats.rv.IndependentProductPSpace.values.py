    @property
    def values(self):
        return sumsets(space.values for space in self.spaces)

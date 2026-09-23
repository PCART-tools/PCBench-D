    @property
    def is_valid(self):
        """ return True if this is a valid field """
        return self.lhs in self.queryables

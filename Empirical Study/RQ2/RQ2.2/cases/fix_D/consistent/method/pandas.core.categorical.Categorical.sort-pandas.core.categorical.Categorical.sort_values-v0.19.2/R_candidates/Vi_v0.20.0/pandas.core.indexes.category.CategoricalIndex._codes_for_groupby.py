    def _codes_for_groupby(self, sort):
        """ Return a Categorical adjusted for groupby """
        return self.values._codes_for_groupby(sort)

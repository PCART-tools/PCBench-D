    def _codes_for_groupby(self, sort, observed):
        """ Return a Categorical adjusted for groupby """
        return self.values._codes_for_groupby(sort, observed)

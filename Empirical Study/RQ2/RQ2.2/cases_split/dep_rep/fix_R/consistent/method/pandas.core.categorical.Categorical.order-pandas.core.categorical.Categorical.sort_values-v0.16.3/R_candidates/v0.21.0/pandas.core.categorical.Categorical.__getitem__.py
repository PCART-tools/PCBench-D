    def __getitem__(self, key):
        """ Return an item. """
        if isinstance(key, (int, np.integer)):
            i = self._codes[key]
            if i == -1:
                return np.nan
            else:
                return self.categories[i]
        else:
            return self._constructor(values=self._codes[key],
                                     categories=self.categories,
                                     ordered=self.ordered, fastpath=True)

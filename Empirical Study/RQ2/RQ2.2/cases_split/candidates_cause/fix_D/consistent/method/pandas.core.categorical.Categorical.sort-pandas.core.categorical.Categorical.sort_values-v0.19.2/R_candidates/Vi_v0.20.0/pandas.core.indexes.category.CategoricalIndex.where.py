    @Appender(_index_shared_docs['where'])
    def where(self, cond, other=None):
        if other is None:
            other = self._na_value
        values = np.where(cond, self.values, other)

        from pandas.core.categorical import Categorical
        cat = Categorical(values,
                          categories=self.categories,
                          ordered=self.ordered)
        return self._shallow_copy(cat, **self._get_attributes_dict())

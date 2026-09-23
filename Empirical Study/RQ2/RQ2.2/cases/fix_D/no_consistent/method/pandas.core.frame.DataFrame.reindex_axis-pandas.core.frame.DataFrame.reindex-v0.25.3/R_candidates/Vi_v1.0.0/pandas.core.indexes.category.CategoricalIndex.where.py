    @Appender(_index_shared_docs["where"])
    def where(self, cond, other=None):
        # TODO: Investigate an alternative implementation with
        # 1. copy the underlying Categorical
        # 2. setitem with `cond` and `other`
        # 3. Rebuild CategoricalIndex.
        if other is None:
            other = self._na_value
        values = np.where(cond, self.values, other)
        cat = Categorical(values, dtype=self.dtype)
        return self._shallow_copy(cat, **self._get_attributes_dict())

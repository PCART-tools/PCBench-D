    def _reindex_non_unique(self, target):
        """
        reindex from a non-unique; which CategoricalIndex's are almost
        always
        """
        new_target, indexer = self.reindex(target)
        new_indexer = None

        check = indexer == -1
        if check.any():
            new_indexer = np.arange(len(self.take(indexer)))
            new_indexer[check] = -1

        cats = self.categories.get_indexer(target)
        if not (cats == -1).any():
            # .reindex returns normal Index. Revert to CategoricalIndex if
            # all targets are included in my categories
            new_target = Categorical(new_target, dtype=self.dtype)
            new_target = type(self)._simple_new(new_target, name=self.name)

        return new_target, indexer, new_indexer

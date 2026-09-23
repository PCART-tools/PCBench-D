    def _reindex_non_unique(  # type: ignore[override]
        self, target: Index
    ) -> tuple[Index, np.ndarray | None, np.ndarray | None]:
        """
        reindex from a non-unique; which CategoricalIndex's are almost
        always
        """
        # TODO: rule out `indexer is None` here to make the signature
        #  match the parent class's signature. This should be equivalent
        #  to ruling out `self.equals(target)`
        new_target, indexer = self.reindex(target)
        new_indexer = None

        check = indexer == -1
        # error: Item "bool" of "Union[Any, bool]" has no attribute "any"
        if check.any():  # type: ignore[union-attr]
            new_indexer = np.arange(len(self.take(indexer)), dtype=np.intp)
            new_indexer[check] = -1

        cats = self.categories.get_indexer(target)
        if not (cats == -1).any():
            # .reindex returns normal Index. Revert to CategoricalIndex if
            # all targets are included in my categories
            cat = Categorical(new_target, dtype=self.dtype)
            new_target = type(self)._simple_new(cat, name=self.name)

        return new_target, indexer, new_indexer

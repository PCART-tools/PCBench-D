    def reindex(
        self, target, method=None, level=None, limit=None, tolerance=None
    ) -> tuple[Index, npt.NDArray[np.intp] | None]:
        """
        Create index with target's values (move/add/delete values as necessary)

        Returns
        -------
        new_index : pd.Index
            Resulting index
        indexer : np.ndarray[np.intp] or None
            Indices of output values in original index

        """
        if method is not None:
            raise NotImplementedError(
                "argument method is not implemented for CategoricalIndex.reindex"
            )
        if level is not None:
            raise NotImplementedError(
                "argument level is not implemented for CategoricalIndex.reindex"
            )
        if limit is not None:
            raise NotImplementedError(
                "argument limit is not implemented for CategoricalIndex.reindex"
            )

        target = ibase.ensure_index(target)

        if self.equals(target):
            indexer = None
            missing = np.array([], dtype=np.intp)
        else:
            indexer, missing = self.get_indexer_non_unique(target)
            if not self.is_unique:
                # GH#42568
                warnings.warn(
                    "reindexing with a non-unique Index is deprecated and will "
                    "raise in a future version.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )

        if len(self) and indexer is not None:
            new_target = self.take(indexer)
        else:
            new_target = target

        # filling in missing if needed
        if len(missing):
            cats = self.categories.get_indexer(target)

            if not isinstance(target, CategoricalIndex) or (cats == -1).any():
                new_target, indexer, _ = super()._reindex_non_unique(target)
            else:

                codes = new_target.codes.copy()
                codes[indexer == -1] = cats[missing]
                cat = self._data._from_backing_data(codes)
                new_target = type(self)._simple_new(cat, name=self.name)

        # we always want to return an Index type here
        # to be consistent with .reindex for other index types (e.g. they don't
        # coerce based on the actual values, only on the dtype)
        # unless we had an initial Categorical to begin with
        # in which case we are going to conform to the passed Categorical
        if is_categorical_dtype(target):
            cat = Categorical(new_target, dtype=target.dtype)
            new_target = type(self)._simple_new(cat, name=self.name)
        else:
            # e.g. test_reindex_with_categoricalindex, test_reindex_duplicate_target
            new_target = np.asarray(new_target)
            new_target = Index._with_infer(new_target, name=self.name)

        return new_target, indexer

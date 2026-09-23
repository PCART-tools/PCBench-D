    def _reorder_indexer(
        self,
        seq: tuple[Scalar | Iterable | AnyArrayLike, ...],
        indexer: npt.NDArray[np.intp],
    ) -> npt.NDArray[np.intp]:
        """
        Reorder an indexer of a MultiIndex (self) so that the labels are in the
        same order as given in seq

        Parameters
        ----------
        seq : label/slice/list/mask or a sequence of such
        indexer: a position indexer of self

        Returns
        -------
        indexer : a sorted position indexer of self ordered as seq
        """

        # check if sorting is necessary
        need_sort = False
        for i, k in enumerate(seq):
            if com.is_null_slice(k) or com.is_bool_indexer(k) or is_scalar(k):
                pass
            elif is_list_like(k):
                if len(k) <= 1:  # type: ignore[arg-type]
                    pass
                elif self._is_lexsorted():
                    # If the index is lexsorted and the list_like label
                    # in seq are sorted then we do not need to sort
                    k_codes = self.levels[i].get_indexer(k)
                    k_codes = k_codes[k_codes >= 0]  # Filter absent keys
                    # True if the given codes are not ordered
                    need_sort = (k_codes[:-1] > k_codes[1:]).any()
                else:
                    need_sort = True
            elif isinstance(k, slice):
                if self._is_lexsorted():
                    need_sort = k.step is not None and k.step < 0
                else:
                    need_sort = True
            else:
                need_sort = True
            if need_sort:
                break
        if not need_sort:
            return indexer

        n = len(self)
        keys: tuple[np.ndarray, ...] = ()
        # For each level of the sequence in seq, map the level codes with the
        # order they appears in a list-like sequence
        # This mapping is then use to reorder the indexer
        for i, k in enumerate(seq):
            if is_scalar(k):
                # GH#34603 we want to treat a scalar the same as an all equal list
                k = [k]
            if com.is_bool_indexer(k):
                new_order = np.arange(n)[indexer]
            elif is_list_like(k):
                # Generate a map with all level codes as sorted initially
                if not isinstance(k, (np.ndarray, ExtensionArray, Index, ABCSeries)):
                    k = sanitize_array(k, None)
                k = algos.unique(k)
                key_order_map = np.ones(len(self.levels[i]), dtype=np.uint64) * len(
                    self.levels[i]
                )
                # Set order as given in the indexer list
                level_indexer = self.levels[i].get_indexer(k)
                level_indexer = level_indexer[level_indexer >= 0]  # Filter absent keys
                key_order_map[level_indexer] = np.arange(len(level_indexer))

                new_order = key_order_map[self.codes[i][indexer]]
            elif isinstance(k, slice) and k.step is not None and k.step < 0:
                # flip order for negative step
                new_order = np.arange(n)[::-1][indexer]
            elif isinstance(k, slice) and k.start is None and k.stop is None:
                # slice(None) should not determine order GH#31330
                new_order = np.ones((n,), dtype=np.intp)[indexer]
            else:
                # For all other case, use the same order as the level
                new_order = np.arange(n)[indexer]
            keys = (new_order,) + keys

        # Find the reordering using lexsort on the keys mapping
        ind = np.lexsort(keys)
        return indexer[ind]

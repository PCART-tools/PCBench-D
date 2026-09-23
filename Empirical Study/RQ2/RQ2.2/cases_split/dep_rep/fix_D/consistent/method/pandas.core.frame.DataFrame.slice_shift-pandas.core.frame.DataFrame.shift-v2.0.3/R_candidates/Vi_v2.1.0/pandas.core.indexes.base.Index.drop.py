    def drop(
        self,
        labels: Index | np.ndarray | Iterable[Hashable],
        errors: IgnoreRaise = "raise",
    ) -> Index:
        """
        Make new Index with passed list of labels deleted.

        Parameters
        ----------
        labels : array-like or scalar
        errors : {'ignore', 'raise'}, default 'raise'
            If 'ignore', suppress error and existing labels are dropped.

        Returns
        -------
        Index
            Will be same type as self, except for RangeIndex.

        Raises
        ------
        KeyError
            If not all of the labels are found in the selected axis

        Examples
        --------
        >>> idx = pd.Index(['a', 'b', 'c'])
        >>> idx.drop(['a'])
        Index(['b', 'c'], dtype='object')
        """
        if not isinstance(labels, Index):
            # avoid materializing e.g. RangeIndex
            arr_dtype = "object" if self.dtype == "object" else None
            labels = com.index_labels_to_array(labels, dtype=arr_dtype)

        indexer = self.get_indexer_for(labels)
        mask = indexer == -1
        if mask.any():
            if errors != "ignore":
                raise KeyError(f"{labels[mask].tolist()} not found in axis")
            indexer = indexer[~mask]
        return self.delete(indexer)

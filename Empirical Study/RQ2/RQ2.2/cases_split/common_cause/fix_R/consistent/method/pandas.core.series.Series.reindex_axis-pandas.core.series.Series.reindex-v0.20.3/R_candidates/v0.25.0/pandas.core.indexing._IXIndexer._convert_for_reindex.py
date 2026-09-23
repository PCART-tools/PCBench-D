    def _convert_for_reindex(self, key, axis: int):
        """
        Transform a list of keys into a new array ready to be used as axis of
        the object we return (e.g. including NaNs).

        Parameters
        ----------
        key : list-like
            Target labels
        axis: int
            Where the indexing is being made

        Returns
        -------
        list-like of labels
        """
        labels = self.obj._get_axis(axis)

        if com.is_bool_indexer(key):
            key = check_bool_indexer(labels, key)
            return labels[key]

        if isinstance(key, Index):
            keyarr = labels._convert_index_indexer(key)
        else:
            # asarray can be unsafe, NumPy strings are weird
            keyarr = com.asarray_tuplesafe(key)

        if is_integer_dtype(keyarr):
            # Cast the indexer to uint64 if possible so
            # that the values returned from indexing are
            # also uint64.
            keyarr = labels._convert_arr_indexer(keyarr)

            if not labels.is_integer():
                keyarr = ensure_platform_int(keyarr)
                return labels.take(keyarr)

        return keyarr

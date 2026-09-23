    def _convert_to_indexer(self, key, axis: int):
        """
        Convert indexing key into something we can use to do actual fancy
        indexing on a ndarray.

        Examples
        ix[:5] -> slice(0, 5)
        ix[[1,2,3]] -> [1,2,3]
        ix[['foo', 'bar', 'baz']] -> [i, j, k] (indices of foo, bar, baz)

        Going by Zen of Python?
        'In the face of ambiguity, refuse the temptation to guess.'
        raise AmbiguousIndexError with integer labels?
        - No, prefer label-based indexing
        """
        labels = self.obj._get_axis(axis)

        if isinstance(key, slice):
            return labels._convert_slice_indexer(key, kind="loc")

        if (
            isinstance(key, tuple)
            and not isinstance(labels, MultiIndex)
            and self.ndim < 2
            and len(key) > 1
        ):
            raise IndexingError("Too many indexers")

        if is_scalar(key) or (isinstance(labels, MultiIndex) and is_hashable(key)):
            # Otherwise get_loc will raise InvalidIndexError

            # if we are a label return me
            try:
                return labels.get_loc(key)
            except LookupError:
                if isinstance(key, tuple) and isinstance(labels, MultiIndex):
                    if len(key) == labels.nlevels:
                        return {"key": key}
                    raise
            except InvalidIndexError:
                # GH35015, using datetime as column indices raises exception
                if not isinstance(labels, MultiIndex):
                    raise
            except ValueError:
                if not is_integer(key):
                    raise
                return {"key": key}

        if is_nested_tuple(key, labels):
            if self.ndim == 1 and any(isinstance(k, tuple) for k in key):
                # GH#35349 Raise if tuple in tuple for series
                raise IndexingError("Too many indexers")
            return labels.get_locs(key)

        elif is_list_like_indexer(key):

            if is_iterator(key):
                key = list(key)

            if com.is_bool_indexer(key):
                key = check_bool_indexer(labels, key)
                return key
            else:
                return self._get_listlike_indexer(key, axis)[1]
        else:
            try:
                return labels.get_loc(key)
            except LookupError:
                # allow a not found key only if we are a setter
                if not is_list_like_indexer(key):
                    return {"key": key}
                raise

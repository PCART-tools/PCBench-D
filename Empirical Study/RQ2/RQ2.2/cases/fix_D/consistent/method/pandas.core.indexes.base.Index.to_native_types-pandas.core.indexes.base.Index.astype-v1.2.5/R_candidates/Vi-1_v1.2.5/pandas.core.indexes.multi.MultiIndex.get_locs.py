    def get_locs(self, seq):
        """
        Get location for a sequence of labels.

        Parameters
        ----------
        seq : label, slice, list, mask or a sequence of such
           You should use one of the above for each level.
           If a level should not be used, set it to ``slice(None)``.

        Returns
        -------
        numpy.ndarray
            NumPy array of integers suitable for passing to iloc.

        See Also
        --------
        MultiIndex.get_loc : Get location for a label or a tuple of labels.
        MultiIndex.slice_locs : Get slice location given start label(s) and
                                end label(s).

        Examples
        --------
        >>> mi = pd.MultiIndex.from_arrays([list('abb'), list('def')])

        >>> mi.get_locs('b')  # doctest: +SKIP
        array([1, 2], dtype=int64)

        >>> mi.get_locs([slice(None), ['e', 'f']])  # doctest: +SKIP
        array([1, 2], dtype=int64)

        >>> mi.get_locs([[True, False, True], slice('e', 'f')])  # doctest: +SKIP
        array([2], dtype=int64)
        """

        # must be lexsorted to at least as many levels
        true_slices = [i for (i, s) in enumerate(com.is_true_slices(seq)) if s]
        if true_slices and true_slices[-1] >= self.lexsort_depth:
            raise UnsortedIndexError(
                "MultiIndex slicing requires the index to be lexsorted: slicing "
                f"on levels {true_slices}, lexsort depth {self.lexsort_depth}"
            )
        # indexer
        # this is the list of all values that we want to select
        n = len(self)
        indexer = None

        def _convert_to_indexer(r) -> Int64Index:
            # return an indexer
            if isinstance(r, slice):
                m = np.zeros(n, dtype=bool)
                m[r] = True
                r = m.nonzero()[0]
            elif com.is_bool_indexer(r):
                if len(r) != n:
                    raise ValueError(
                        "cannot index with a boolean indexer "
                        "that is not the same length as the "
                        "index"
                    )
                r = r.nonzero()[0]
            return Int64Index(r)

        def _update_indexer(
            idxr: Optional[Index], indexer: Optional[Index], key
        ) -> Index:
            if indexer is None:
                indexer = Index(np.arange(n))
            if idxr is None:
                return indexer
            indexer_intersection = indexer.intersection(idxr)
            if indexer_intersection.empty and not idxr.empty and not indexer.empty:
                raise KeyError(key)
            return indexer_intersection

        for i, k in enumerate(seq):

            if com.is_bool_indexer(k):
                # a boolean indexer, must be the same length!
                k = np.asarray(k)
                indexer = _update_indexer(
                    _convert_to_indexer(k), indexer=indexer, key=seq
                )

            elif is_list_like(k):
                # a collection of labels to include from this level (these
                # are or'd)
                indexers: Optional[Int64Index] = None
                for x in k:
                    try:
                        idxrs = _convert_to_indexer(
                            self._get_level_indexer(x, level=i, indexer=indexer)
                        )
                        indexers = (idxrs if indexers is None else indexers).union(
                            idxrs, sort=False
                        )
                    except KeyError:

                        # ignore not founds
                        continue

                if indexers is not None:
                    indexer = _update_indexer(indexers, indexer=indexer, key=seq)
                else:
                    # no matches we are done
                    return np.array([], dtype=np.int64)

            elif com.is_null_slice(k):
                # empty slice
                indexer = _update_indexer(None, indexer=indexer, key=seq)

            elif isinstance(k, slice):

                # a slice, include BOTH of the labels
                indexer = _update_indexer(
                    _convert_to_indexer(
                        self._get_level_indexer(k, level=i, indexer=indexer)
                    ),
                    indexer=indexer,
                    key=seq,
                )
            else:
                # a single label
                indexer = _update_indexer(
                    _convert_to_indexer(
                        self.get_loc_level(k, level=i, drop_level=False)[0]
                    ),
                    indexer=indexer,
                    key=seq,
                )

        # empty indexer
        if indexer is None:
            return np.array([], dtype=np.int64)

        assert isinstance(indexer, Int64Index), type(indexer)
        indexer = self._reorder_indexer(seq, indexer)

        return indexer._values

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
        if true_slices and true_slices[-1] >= self._lexsort_depth:
            raise UnsortedIndexError(
                "MultiIndex slicing requires the index to be lexsorted: slicing "
                f"on levels {true_slices}, lexsort depth {self._lexsort_depth}"
            )

        n = len(self)
        # indexer is the list of all positions that we want to take; we
        #  start with it being everything and narrow it down as we look at each
        #  entry in `seq`
        indexer = Index(np.arange(n))

        if any(x is Ellipsis for x in seq):
            raise NotImplementedError(
                "MultiIndex does not support indexing with Ellipsis"
            )

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

        def _update_indexer(idxr: Index, indexer: Index) -> Index:
            indexer_intersection = indexer.intersection(idxr)
            if indexer_intersection.empty and not idxr.empty and not indexer.empty:
                raise KeyError(seq)
            return indexer_intersection

        for i, k in enumerate(seq):

            if com.is_bool_indexer(k):
                # a boolean indexer, must be the same length!
                k = np.asarray(k)
                lvl_indexer = _convert_to_indexer(k)
                indexer = _update_indexer(lvl_indexer, indexer=indexer)

            elif is_list_like(k):
                # a collection of labels to include from this level (these
                # are or'd)

                indexers: Int64Index | None = None

                # GH#27591 check if this is a single tuple key in the level
                try:
                    # Argument "indexer" to "_get_level_indexer" of "MultiIndex"
                    # has incompatible type "Index"; expected "Optional[Int64Index]"
                    lev_loc = self._get_level_indexer(
                        k, level=i, indexer=indexer  # type: ignore[arg-type]
                    )
                except (InvalidIndexError, TypeError, KeyError) as err:
                    # InvalidIndexError e.g. non-hashable, fall back to treating
                    #  this as a sequence of labels
                    # KeyError it can be ambiguous if this is a label or sequence
                    #  of labels
                    #  github.com/pandas-dev/pandas/issues/39424#issuecomment-871626708
                    for x in k:
                        if not is_hashable(x):
                            # e.g. slice
                            raise err
                        try:
                            # Argument "indexer" to "_get_level_indexer" of "MultiIndex"
                            # has incompatible type "Index"; expected
                            # "Optional[Int64Index]"
                            item_lvl_indexer = self._get_level_indexer(
                                x, level=i, indexer=indexer  # type: ignore[arg-type]
                            )
                        except KeyError:
                            # ignore not founds; see discussion in GH#39424
                            warnings.warn(
                                "The behavior of indexing on a MultiIndex with a "
                                "nested sequence of labels is deprecated and will "
                                "change in a future version. "
                                "`series.loc[label, sequence]` will raise if any "
                                "members of 'sequence' or not present in "
                                "the index's second level. To retain the old "
                                "behavior, use `series.index.isin(sequence, level=1)`",
                                # TODO: how to opt in to the future behavior?
                                # TODO: how to handle IntervalIndex level?
                                #  (no test cases)
                                FutureWarning,
                                stacklevel=find_stack_level(),
                            )
                            continue
                        else:
                            idxrs = _convert_to_indexer(item_lvl_indexer)

                            if indexers is None:
                                indexers = idxrs
                            else:
                                indexers = indexers.union(idxrs, sort=False)

                else:
                    idxrs = _convert_to_indexer(lev_loc)
                    if indexers is None:
                        indexers = idxrs
                    else:
                        indexers = indexers.union(idxrs, sort=False)

                if indexers is not None:
                    indexer = _update_indexer(indexers, indexer=indexer)
                else:
                    # no matches we are done
                    # test_loc_getitem_duplicates_multiindex_empty_indexer
                    return np.array([], dtype=np.intp)

            elif com.is_null_slice(k):
                # empty slice
                pass

            elif isinstance(k, slice):

                # a slice, include BOTH of the labels
                # Argument "indexer" to "_get_level_indexer" of "MultiIndex" has
                # incompatible type "Index"; expected "Optional[Int64Index]"
                lvl_indexer = self._get_level_indexer(
                    k,
                    level=i,
                    indexer=indexer,  # type: ignore[arg-type]
                )
                indexer = _update_indexer(
                    _convert_to_indexer(lvl_indexer),
                    indexer=indexer,
                )
            else:
                # a single label
                lvl_indexer = self._get_loc_level(k, level=i)[0]
                indexer = _update_indexer(
                    _convert_to_indexer(lvl_indexer),
                    indexer=indexer,
                )

        # empty indexer
        if indexer is None:
            return np.array([], dtype=np.intp)

        assert isinstance(indexer, Int64Index), type(indexer)
        indexer = self._reorder_indexer(seq, indexer)

        return indexer._values.astype(np.intp, copy=False)

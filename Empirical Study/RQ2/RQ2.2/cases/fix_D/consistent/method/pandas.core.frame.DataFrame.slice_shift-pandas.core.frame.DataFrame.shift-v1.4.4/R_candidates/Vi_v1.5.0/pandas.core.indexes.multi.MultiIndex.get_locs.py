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

        if any(x is Ellipsis for x in seq):
            raise NotImplementedError(
                "MultiIndex does not support indexing with Ellipsis"
            )

        n = len(self)

        def _to_bool_indexer(indexer) -> npt.NDArray[np.bool_]:
            if isinstance(indexer, slice):
                new_indexer = np.zeros(n, dtype=np.bool_)
                new_indexer[indexer] = True
                return new_indexer
            return indexer

        # a bool indexer for the positions we want to take
        indexer: npt.NDArray[np.bool_] | None = None

        for i, k in enumerate(seq):

            lvl_indexer: npt.NDArray[np.bool_] | slice | None = None

            if com.is_bool_indexer(k):
                if len(k) != n:
                    raise ValueError(
                        "cannot index with a boolean indexer that "
                        "is not the same length as the index"
                    )
                lvl_indexer = np.asarray(k)

            elif is_list_like(k):
                # a collection of labels to include from this level (these are or'd)

                # GH#27591 check if this is a single tuple key in the level
                try:
                    lvl_indexer = self._get_level_indexer(k, level=i, indexer=indexer)
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
                            item_indexer = self._get_level_indexer(
                                x, level=i, indexer=indexer
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
                                stacklevel=find_stack_level(inspect.currentframe()),
                            )
                            continue
                        else:
                            if lvl_indexer is None:
                                lvl_indexer = _to_bool_indexer(item_indexer)
                            elif isinstance(item_indexer, slice):
                                lvl_indexer[item_indexer] = True  # type: ignore[index]
                            else:
                                lvl_indexer |= item_indexer

                if lvl_indexer is None:
                    # no matches we are done
                    # test_loc_getitem_duplicates_multiindex_empty_indexer
                    return np.array([], dtype=np.intp)

            elif com.is_null_slice(k):
                # empty slice
                if indexer is None and i == len(seq) - 1:
                    return np.arange(n, dtype=np.intp)
                continue

            else:
                # a slice or a single label
                lvl_indexer = self._get_level_indexer(k, level=i, indexer=indexer)

            # update indexer
            lvl_indexer = _to_bool_indexer(lvl_indexer)
            if indexer is None:
                indexer = lvl_indexer
            else:
                indexer &= lvl_indexer
                if not np.any(indexer) and np.any(lvl_indexer):
                    raise KeyError(seq)

        # empty indexer
        if indexer is None:
            return np.array([], dtype=np.intp)

        pos_indexer = indexer.nonzero()[0]
        return self._reorder_indexer(seq, pos_indexer)

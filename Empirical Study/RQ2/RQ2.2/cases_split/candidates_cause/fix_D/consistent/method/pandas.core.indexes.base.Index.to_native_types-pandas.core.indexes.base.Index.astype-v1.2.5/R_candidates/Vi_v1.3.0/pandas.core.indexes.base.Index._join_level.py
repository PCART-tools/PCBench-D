    @final
    def _join_level(
        self, other: Index, level, how: str_t = "left", keep_order: bool = True
    ) -> tuple[MultiIndex, np.ndarray | None, np.ndarray | None]:
        # Any returned ndarrays are np.intp
        """
        The join method *only* affects the level of the resulting
        MultiIndex. Otherwise it just exactly aligns the Index data to the
        labels of the level in the MultiIndex.

        If ```keep_order == True```, the order of the data indexed by the
        MultiIndex will not be changed; otherwise, it will tie out
        with `other`.
        """
        from pandas.core.indexes.multi import MultiIndex

        def _get_leaf_sorter(labels: list[np.ndarray]) -> np.ndarray:
            """
            Returns sorter for the inner most level while preserving the
            order of higher levels.

            Parameters
            ----------
            labels : list[np.ndarray]
                Each ndarray has signed integer dtype, not necessarily identical.

            Returns
            -------
            np.ndarray[np.intp]
            """
            if labels[0].size == 0:
                return np.empty(0, dtype=np.intp)

            if len(labels) == 1:
                return get_group_index_sorter(ensure_platform_int(labels[0]))

            # find indexers of beginning of each set of
            # same-key labels w.r.t all but last level
            tic = labels[0][:-1] != labels[0][1:]
            for lab in labels[1:-1]:
                tic |= lab[:-1] != lab[1:]

            starts = np.hstack(([True], tic, [True])).nonzero()[0]
            lab = ensure_int64(labels[-1])
            return lib.get_level_sorter(lab, ensure_platform_int(starts))

        if isinstance(self, MultiIndex) and isinstance(other, MultiIndex):
            raise TypeError("Join on level between two MultiIndex objects is ambiguous")

        left, right = self, other

        flip_order = not isinstance(self, MultiIndex)
        if flip_order:
            left, right = right, left
            how = {"right": "left", "left": "right"}.get(how, how)

        assert isinstance(left, MultiIndex)

        level = left._get_level_number(level)
        old_level = left.levels[level]

        if not right.is_unique:
            raise NotImplementedError(
                "Index._join_level on non-unique index is not implemented"
            )

        new_level, left_lev_indexer, right_lev_indexer = old_level.join(
            right, how=how, return_indexers=True
        )

        if left_lev_indexer is None:
            if keep_order or len(left) == 0:
                left_indexer = None
                join_index = left
            else:  # sort the leaves
                left_indexer = _get_leaf_sorter(left.codes[: level + 1])
                join_index = left[left_indexer]

        else:
            left_lev_indexer = ensure_platform_int(left_lev_indexer)
            rev_indexer = lib.get_reverse_indexer(left_lev_indexer, len(old_level))
            old_codes = left.codes[level]

            taker = old_codes[old_codes != -1]
            new_lev_codes = rev_indexer.take(taker)

            new_codes = list(left.codes)
            new_codes[level] = new_lev_codes

            new_levels = list(left.levels)
            new_levels[level] = new_level

            if keep_order:  # just drop missing values. o.w. keep order
                left_indexer = np.arange(len(left), dtype=np.intp)
                left_indexer = cast(np.ndarray, left_indexer)
                mask = new_lev_codes != -1
                if not mask.all():
                    new_codes = [lab[mask] for lab in new_codes]
                    left_indexer = left_indexer[mask]

            else:  # tie out the order with other
                if level == 0:  # outer most level, take the fast route
                    max_new_lev = 0 if len(new_lev_codes) == 0 else new_lev_codes.max()
                    ngroups = 1 + max_new_lev
                    left_indexer, counts = libalgos.groupsort_indexer(
                        new_lev_codes, ngroups
                    )

                    # missing values are placed first; drop them!
                    left_indexer = left_indexer[counts[0] :]
                    new_codes = [lab[left_indexer] for lab in new_codes]

                else:  # sort the leaves
                    mask = new_lev_codes != -1
                    mask_all = mask.all()
                    if not mask_all:
                        new_codes = [lab[mask] for lab in new_codes]

                    left_indexer = _get_leaf_sorter(new_codes[: level + 1])
                    new_codes = [lab[left_indexer] for lab in new_codes]

                    # left_indexers are w.r.t masked frame.
                    # reverse to original frame!
                    if not mask_all:
                        left_indexer = mask.nonzero()[0][left_indexer]

            join_index = MultiIndex(
                levels=new_levels,
                codes=new_codes,
                names=left.names,
                verify_integrity=False,
            )

        if right_lev_indexer is not None:
            right_indexer = right_lev_indexer.take(join_index.codes[level])
        else:
            right_indexer = join_index.codes[level]

        if flip_order:
            left_indexer, right_indexer = right_indexer, left_indexer

        left_indexer = (
            None if left_indexer is None else ensure_platform_int(left_indexer)
        )
        right_indexer = (
            None if right_indexer is None else ensure_platform_int(right_indexer)
        )
        return join_index, left_indexer, right_indexer

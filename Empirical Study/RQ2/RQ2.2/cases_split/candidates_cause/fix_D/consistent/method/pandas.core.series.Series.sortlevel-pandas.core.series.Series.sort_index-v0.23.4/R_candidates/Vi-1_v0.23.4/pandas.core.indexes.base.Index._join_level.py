    def _join_level(self, other, level, how='left', return_indexers=False,
                    keep_order=True):
        """
        The join method *only* affects the level of the resulting
        MultiIndex. Otherwise it just exactly aligns the Index data to the
        labels of the level in the MultiIndex. If `keep_order` == True, the
        order of the data indexed by the MultiIndex will not be changed;
        otherwise, it will tie out with `other`.
        """
        from .multi import MultiIndex

        def _get_leaf_sorter(labels):
            """
            returns sorter for the inner most level while preserving the
            order of higher levels
            """
            if labels[0].size == 0:
                return np.empty(0, dtype='int64')

            if len(labels) == 1:
                lab = _ensure_int64(labels[0])
                sorter, _ = libalgos.groupsort_indexer(lab, 1 + lab.max())
                return sorter

            # find indexers of beginning of each set of
            # same-key labels w.r.t all but last level
            tic = labels[0][:-1] != labels[0][1:]
            for lab in labels[1:-1]:
                tic |= lab[:-1] != lab[1:]

            starts = np.hstack(([True], tic, [True])).nonzero()[0]
            lab = _ensure_int64(labels[-1])
            return lib.get_level_sorter(lab, _ensure_int64(starts))

        if isinstance(self, MultiIndex) and isinstance(other, MultiIndex):
            raise TypeError('Join on level between two MultiIndex objects '
                            'is ambiguous')

        left, right = self, other

        flip_order = not isinstance(self, MultiIndex)
        if flip_order:
            left, right = right, left
            how = {'right': 'left', 'left': 'right'}.get(how, how)

        level = left._get_level_number(level)
        old_level = left.levels[level]

        if not right.is_unique:
            raise NotImplementedError('Index._join_level on non-unique index '
                                      'is not implemented')

        new_level, left_lev_indexer, right_lev_indexer = \
            old_level.join(right, how=how, return_indexers=True)

        if left_lev_indexer is None:
            if keep_order or len(left) == 0:
                left_indexer = None
                join_index = left
            else:  # sort the leaves
                left_indexer = _get_leaf_sorter(left.labels[:level + 1])
                join_index = left[left_indexer]

        else:
            left_lev_indexer = _ensure_int64(left_lev_indexer)
            rev_indexer = lib.get_reverse_indexer(left_lev_indexer,
                                                  len(old_level))

            new_lev_labels = algos.take_nd(rev_indexer, left.labels[level],
                                           allow_fill=False)

            new_labels = list(left.labels)
            new_labels[level] = new_lev_labels

            new_levels = list(left.levels)
            new_levels[level] = new_level

            if keep_order:  # just drop missing values. o.w. keep order
                left_indexer = np.arange(len(left), dtype=np.intp)
                mask = new_lev_labels != -1
                if not mask.all():
                    new_labels = [lab[mask] for lab in new_labels]
                    left_indexer = left_indexer[mask]

            else:  # tie out the order with other
                if level == 0:  # outer most level, take the fast route
                    ngroups = 1 + new_lev_labels.max()
                    left_indexer, counts = libalgos.groupsort_indexer(
                        new_lev_labels, ngroups)

                    # missing values are placed first; drop them!
                    left_indexer = left_indexer[counts[0]:]
                    new_labels = [lab[left_indexer] for lab in new_labels]

                else:  # sort the leaves
                    mask = new_lev_labels != -1
                    mask_all = mask.all()
                    if not mask_all:
                        new_labels = [lab[mask] for lab in new_labels]

                    left_indexer = _get_leaf_sorter(new_labels[:level + 1])
                    new_labels = [lab[left_indexer] for lab in new_labels]

                    # left_indexers are w.r.t masked frame.
                    # reverse to original frame!
                    if not mask_all:
                        left_indexer = mask.nonzero()[0][left_indexer]

            join_index = MultiIndex(levels=new_levels, labels=new_labels,
                                    names=left.names, verify_integrity=False)

        if right_lev_indexer is not None:
            right_indexer = algos.take_nd(right_lev_indexer,
                                          join_index.labels[level],
                                          allow_fill=False)
        else:
            right_indexer = join_index.labels[level]

        if flip_order:
            left_indexer, right_indexer = right_indexer, left_indexer

        if return_indexers:
            left_indexer = (None if left_indexer is None
                            else _ensure_platform_int(left_indexer))
            right_indexer = (None if right_indexer is None
                             else _ensure_platform_int(right_indexer))
            return join_index, left_indexer, right_indexer
        else:
            return join_index

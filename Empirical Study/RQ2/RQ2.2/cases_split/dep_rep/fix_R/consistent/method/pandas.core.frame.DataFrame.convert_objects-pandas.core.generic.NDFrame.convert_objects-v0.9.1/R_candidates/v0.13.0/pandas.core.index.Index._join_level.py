    def _join_level(self, other, level, how='left', return_indexers=False):
        """
        The join method *only* affects the level of the resulting
        MultiIndex. Otherwise it just exactly aligns the Index data to the
        labels of the level in the MultiIndex. The order of the data indexed by
        the MultiIndex will not be changed (currently)
        """
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

        new_level, left_lev_indexer, right_lev_indexer = \
            old_level.join(right, how=how, return_indexers=True)

        if left_lev_indexer is not None:
            left_lev_indexer = com._ensure_int64(left_lev_indexer)
            rev_indexer = lib.get_reverse_indexer(left_lev_indexer,
                                                  len(old_level))

            new_lev_labels = com.take_nd(rev_indexer, left.labels[level],
                                         allow_fill=False)
            omit_mask = new_lev_labels != -1

            new_labels = list(left.labels)
            new_labels[level] = new_lev_labels

            if not omit_mask.all():
                new_labels = [lab[omit_mask] for lab in new_labels]

            new_levels = list(left.levels)
            new_levels[level] = new_level

            join_index = MultiIndex(levels=new_levels, labels=new_labels,
                                    names=left.names, verify_integrity=False)
            left_indexer = np.arange(len(left))[new_lev_labels != -1]
        else:
            join_index = left
            left_indexer = None

        if right_lev_indexer is not None:
            right_indexer = com.take_nd(right_lev_indexer,
                                        join_index.labels[level],
                                        allow_fill=False)
        else:
            right_indexer = join_index.labels[level]

        if flip_order:
            left_indexer, right_indexer = right_indexer, left_indexer

        if return_indexers:
            return join_index, left_indexer, right_indexer
        else:
            return join_index

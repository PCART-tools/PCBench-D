    def _join_non_unique(self, other, how='left', return_indexers=False):
        from pandas.core.reshape.merge import _get_join_indexers

        left_idx, right_idx = _get_join_indexers([self._ndarray_values],
                                                 [other._ndarray_values],
                                                 how=how,
                                                 sort=True)

        left_idx = ensure_platform_int(left_idx)
        right_idx = ensure_platform_int(right_idx)

        join_index = np.asarray(self._ndarray_values.take(left_idx))
        mask = left_idx == -1
        np.putmask(join_index, mask, other._ndarray_values.take(right_idx))

        join_index = self._wrap_joined_index(join_index, other)

        if return_indexers:
            return join_index, left_idx, right_idx
        else:
            return join_index

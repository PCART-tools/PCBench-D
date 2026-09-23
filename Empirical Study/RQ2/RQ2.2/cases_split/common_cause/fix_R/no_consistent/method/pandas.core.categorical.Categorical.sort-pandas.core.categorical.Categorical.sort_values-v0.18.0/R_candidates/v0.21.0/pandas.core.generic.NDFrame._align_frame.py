    def _align_frame(self, other, join='outer', axis=None, level=None,
                     copy=True, fill_value=np.nan, method=None, limit=None,
                     fill_axis=0):
        # defaults
        join_index, join_columns = None, None
        ilidx, iridx = None, None
        clidx, cridx = None, None

        is_series = isinstance(self, ABCSeries)

        if axis is None or axis == 0:
            if not self.index.equals(other.index):
                join_index, ilidx, iridx = self.index.join(
                    other.index, how=join, level=level, return_indexers=True)

        if axis is None or axis == 1:
            if not is_series and not self.columns.equals(other.columns):
                join_columns, clidx, cridx = self.columns.join(
                    other.columns, how=join, level=level, return_indexers=True)

        if is_series:
            reindexers = {0: [join_index, ilidx]}
        else:
            reindexers = {0: [join_index, ilidx], 1: [join_columns, clidx]}

        left = self._reindex_with_indexers(reindexers, copy=copy,
                                           fill_value=fill_value,
                                           allow_dups=True)
        # other must be always DataFrame
        right = other._reindex_with_indexers({0: [join_index, iridx],
                                              1: [join_columns, cridx]},
                                             copy=copy, fill_value=fill_value,
                                             allow_dups=True)

        if method is not None:
            left = left.fillna(axis=fill_axis, method=method, limit=limit)
            right = right.fillna(axis=fill_axis, method=method, limit=limit)

        # if DatetimeIndex have different tz, convert to UTC
        if is_datetime64tz_dtype(left.index):
            if left.index.tz != right.index.tz:
                if join_index is not None:
                    left.index = join_index
                    right.index = join_index

        return left.__finalize__(self), right.__finalize__(other)

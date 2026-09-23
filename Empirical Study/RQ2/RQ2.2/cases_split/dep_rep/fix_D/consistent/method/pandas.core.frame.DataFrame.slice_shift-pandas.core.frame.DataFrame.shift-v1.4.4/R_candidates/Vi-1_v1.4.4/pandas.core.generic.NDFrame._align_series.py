    @final
    def _align_series(
        self,
        other,
        join="outer",
        axis=None,
        level=None,
        copy: bool_t = True,
        fill_value=None,
        method=None,
        limit=None,
        fill_axis=0,
    ):

        is_series = isinstance(self, ABCSeries)

        # series/series compat, other must always be a Series
        if is_series:
            if axis:
                raise ValueError("cannot align series to a series other than axis 0")

            # equal
            if self.index.equals(other.index):
                join_index, lidx, ridx = None, None, None
            else:
                join_index, lidx, ridx = self.index.join(
                    other.index, how=join, level=level, return_indexers=True
                )

            left = self._reindex_indexer(join_index, lidx, copy)
            right = other._reindex_indexer(join_index, ridx, copy)

        else:
            # one has > 1 ndim
            fdata = self._mgr
            if axis in [0, 1]:
                join_index = self.axes[axis]
                lidx, ridx = None, None
                if not join_index.equals(other.index):
                    join_index, lidx, ridx = join_index.join(
                        other.index, how=join, level=level, return_indexers=True
                    )

                if lidx is not None:
                    bm_axis = self._get_block_manager_axis(axis)
                    fdata = fdata.reindex_indexer(join_index, lidx, axis=bm_axis)

            else:
                raise ValueError("Must specify axis=0 or 1")

            if copy and fdata is self._mgr:
                fdata = fdata.copy()

            left = self._constructor(fdata)

            if ridx is None:
                right = other
            else:
                right = other.reindex(join_index, level=level)

        # fill
        fill_na = notna(fill_value) or (method is not None)
        if fill_na:
            left = left.fillna(fill_value, method=method, limit=limit, axis=fill_axis)
            right = right.fillna(fill_value, method=method, limit=limit)

        # if DatetimeIndex have different tz, convert to UTC
        if is_series or (not is_series and axis == 0):
            left, right = _align_as_utc(left, right, join_index)

        return (
            left.__finalize__(self),
            right.__finalize__(other),
        )

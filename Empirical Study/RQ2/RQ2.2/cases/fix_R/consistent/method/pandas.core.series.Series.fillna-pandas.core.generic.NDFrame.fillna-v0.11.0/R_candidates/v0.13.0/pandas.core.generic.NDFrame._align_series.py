    def _align_series(self, other, join='outer', axis=None, level=None,
                      copy=True, fill_value=None, method=None, limit=None,
                      fill_axis=0):
        from pandas import DataFrame

        # series/series compat
        if isinstance(self, ABCSeries) and isinstance(other, ABCSeries):
            if axis:
                raise ValueError('cannot align series to a series other than '
                                 'axis 0')

            join_index, lidx, ridx = self.index.join(other.index, how=join,
                                                     level=level,
                                                     return_indexers=True)

            left_result = self._reindex_indexer(join_index, lidx, copy)
            right_result = other._reindex_indexer(join_index, ridx, copy)

        else:

            # one has > 1 ndim
            fdata = self._data
            if axis == 0:
                join_index = self.index
                lidx, ridx = None, None
                if not self.index.equals(other.index):
                    join_index, lidx, ridx = self.index.join(
                        other.index, how=join, return_indexers=True)

                if lidx is not None:
                    fdata = fdata.reindex_indexer(join_index, lidx, axis=1)
            elif axis == 1:
                join_index = self.columns
                lidx, ridx = None, None
                if not self.columns.equals(other.index):
                    join_index, lidx, ridx = \
                        self.columns.join(other.index, how=join,
                                          return_indexers=True)

                if lidx is not None:
                    fdata = fdata.reindex_indexer(join_index, lidx, axis=0)
            else:
                raise ValueError('Must specify axis=0 or 1')

            if copy and fdata is self._data:
                fdata = fdata.copy()

            left_result = DataFrame(fdata)
            right_result = other if ridx is None else other.reindex(join_index)

        # fill
        fill_na = notnull(fill_value) or (method is not None)
        if fill_na:
            return (left_result.fillna(fill_value, method=method, limit=limit,
                                       axis=fill_axis),
                    right_result.fillna(fill_value, method=method,
                                        limit=limit))
        else:
            return (left_result.__finalize__(self),
                    right_result.__finalize__(other))

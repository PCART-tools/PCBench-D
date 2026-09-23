    def reindex_axis(self, new_axis, indexer=None, method=None, axis=0,
                     fill_value=None, limit=None, copy=True):
        new_axis = _ensure_index(new_axis)
        cur_axis = self.axes[axis]

        if new_axis.equals(cur_axis):
            if copy:
                result = self.copy(deep=True)
                result.axes[axis] = new_axis
                result._shape = None

                if axis == 0:
                    # patch ref_items, #1823
                    for blk in result.blocks:
                        blk.ref_items = new_axis

                return result
            else:
                return self

        if axis == 0:
            if method is not None or limit is not None:
                return self.reindex_axis0_with_method(
                    new_axis, indexer=indexer, method=method,
                    fill_value=fill_value, limit=limit, copy=copy
                )
            return self.reindex_items(new_axis, indexer=indexer, copy=copy,
                                      fill_value=fill_value)

        new_axis, indexer = cur_axis.reindex(
            new_axis, method, copy_if_needed=True)
        return self.reindex_indexer(new_axis, indexer, axis=axis,
                                    fill_value=fill_value)

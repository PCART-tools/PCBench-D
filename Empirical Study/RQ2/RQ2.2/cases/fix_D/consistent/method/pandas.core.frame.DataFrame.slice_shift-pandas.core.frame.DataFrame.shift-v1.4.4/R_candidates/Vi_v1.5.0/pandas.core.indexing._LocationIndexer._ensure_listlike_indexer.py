    @final
    def _ensure_listlike_indexer(self, key, axis=None, value=None):
        """
        Ensure that a list-like of column labels are all present by adding them if
        they do not already exist.

        Parameters
        ----------
        key : list-like of column labels
            Target labels.
        axis : key axis if known
        """
        column_axis = 1

        # column only exists in 2-dimensional DataFrame
        if self.ndim != 2:
            return

        if isinstance(key, tuple) and len(key) > 1:
            # key may be a tuple if we are .loc
            # if length of key is > 1 set key to column part
            key = key[column_axis]
            axis = column_axis

        if (
            axis == column_axis
            and not isinstance(self.obj.columns, MultiIndex)
            and is_list_like_indexer(key)
            and not com.is_bool_indexer(key)
            and all(is_hashable(k) for k in key)
        ):
            # GH#38148
            keys = self.obj.columns.union(key, sort=False)

            self.obj._mgr = self.obj._mgr.reindex_axis(keys, axis=0, only_slice=True)

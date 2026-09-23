    def _set_item_frame_value(self, key, value: DataFrame) -> None:
        self._ensure_valid_index(value)

        # align columns
        if key in self.columns:
            loc = self.columns.get_loc(key)
            cols = self.columns[loc]
            len_cols = 1 if is_scalar(cols) else len(cols)
            if len_cols != len(value.columns):
                raise ValueError("Columns must be same length as key")

            # align right-hand-side columns if self.columns
            # is multi-index and self[key] is a sub-frame
            if isinstance(self.columns, MultiIndex) and isinstance(
                loc, (slice, Series, np.ndarray, Index)
            ):
                cols = maybe_droplevels(cols, key)
                if len(cols) and not cols.equals(value.columns):
                    value = value.reindex(cols, axis=1)

        # now align rows
        arraylike = _reindex_for_setitem(value, self.index)
        self._set_item_mgr(key, arraylike)

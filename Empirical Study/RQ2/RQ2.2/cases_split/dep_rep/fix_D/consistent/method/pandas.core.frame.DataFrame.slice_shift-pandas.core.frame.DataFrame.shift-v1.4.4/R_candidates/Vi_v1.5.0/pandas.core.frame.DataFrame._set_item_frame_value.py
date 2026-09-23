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
                cols_droplevel = maybe_droplevels(cols, key)
                if len(cols_droplevel) and not cols_droplevel.equals(value.columns):
                    value = value.reindex(cols_droplevel, axis=1)

                for col, col_droplevel in zip(cols, cols_droplevel):
                    self[col] = value[col_droplevel]
                return

            if is_scalar(cols):
                self[cols] = value[value.columns[0]]
                return

            # now align rows
            arraylike = _reindex_for_setitem(value, self.index)
            self._set_item_mgr(key, arraylike)
            return

        if len(value.columns) != 1:
            raise ValueError(
                "Cannot set a DataFrame with multiple columns to the single "
                f"column {key}"
            )

        self[key] = value[value.columns[0]]

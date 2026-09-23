    def _set_item(self, key, value) -> None:
        """
        Add series to DataFrame in specified column.

        If series is a numpy-array (not a Series/TimeSeries), it must be the
        same length as the DataFrames index or an error will be thrown.

        Series/TimeSeries will be conformed to the DataFrames index to
        ensure homogeneity.
        """
        value, refs = self._sanitize_column(value)

        if (
            key in self.columns
            and value.ndim == 1
            and not isinstance(value.dtype, ExtensionDtype)
        ):
            # broadcast across multiple columns if necessary
            if not self.columns.is_unique or isinstance(self.columns, MultiIndex):
                existing_piece = self[key]
                if isinstance(existing_piece, DataFrame):
                    value = np.tile(value, (len(existing_piece.columns), 1)).T
                    refs = None

        self._set_item_mgr(key, value, refs)

    def _setitem_with_indexer_2d_value(self, indexer, value):
        # We get here with np.ndim(value) == 2, excluding DataFrame,
        #  which goes through _setitem_with_indexer_frame_value
        pi = indexer[0]

        ilocs = self._ensure_iterable_column_indexer(indexer[1])

        if not is_array_like(value):
            # cast lists to array
            value = np.array(value, dtype=object)
        if len(ilocs) != value.shape[1]:
            raise ValueError(
                "Must have equal len keys and value when setting with an ndarray"
            )

        for i, loc in enumerate(ilocs):
            value_col = value[:, i]
            if is_object_dtype(value_col.dtype):
                # casting to list so that we do type inference in setitem_single_column
                value_col = value_col.tolist()
            self._setitem_single_column(loc, value_col, pi)

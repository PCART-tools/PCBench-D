    def _setitem_with_indexer_2d_value(self, indexer, value):
        # We get here with np.ndim(value) == 2, excluding DataFrame,
        #  which goes through _setitem_with_indexer_frame_value
        pi = indexer[0]

        ilocs = self._ensure_iterable_column_indexer(indexer[1])

        # GH#7551 Note that this coerces the dtype if we are mixed
        value = np.array(value, dtype=object)
        if len(ilocs) != value.shape[1]:
            raise ValueError(
                "Must have equal len keys and value when setting with an ndarray"
            )

        for i, loc in enumerate(ilocs):
            # setting with a list, re-coerces
            self._setitem_single_column(loc, value[:, i].tolist(), pi)

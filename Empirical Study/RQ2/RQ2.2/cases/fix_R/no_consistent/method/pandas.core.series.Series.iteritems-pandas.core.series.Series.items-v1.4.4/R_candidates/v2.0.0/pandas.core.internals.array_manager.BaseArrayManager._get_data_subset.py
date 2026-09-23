    def _get_data_subset(self: T, predicate: Callable) -> T:
        indices = [i for i, arr in enumerate(self.arrays) if predicate(arr)]
        arrays = [self.arrays[i] for i in indices]
        # TODO copy?
        # Note: using Index.take ensures we can retain e.g. DatetimeIndex.freq,
        #  see test_describe_datetime_columns
        taker = np.array(indices, dtype="intp")
        new_cols = self._axes[1].take(taker)
        new_axes = [self._axes[0], new_cols]
        return type(self)(arrays, new_axes, verify_integrity=False)

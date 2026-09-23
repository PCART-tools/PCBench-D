    @final
    def _maybe_transpose_result(self, result: NDFrameT) -> NDFrameT:
        if self.axis == 1:
            # Only relevant for DataFrameGroupBy, no-op for SeriesGroupBy
            result = result.T
            if result.index.equals(self.obj.index):
                # Retain e.g. DatetimeIndex/TimedeltaIndex freq
                # e.g. test_groupby_crash_on_nunique
                result.index = self.obj.index.copy()
        return result

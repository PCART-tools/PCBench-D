    @final
    def _set_result_index_ordered(
        self, result: OutputFrameOrSeries
    ) -> OutputFrameOrSeries:
        # set the result index on the passed values object and
        # return the new object, xref 8046

        obj_axis = self.obj._get_axis(self.axis)

        if self.grouper.is_monotonic and not self.grouper.has_dropped_na:
            # shortcut if we have an already ordered grouper
            result = result.set_axis(obj_axis, axis=self.axis, copy=False)
            return result

        # row order is scrambled => sort the rows by position in original index
        original_positions = Index(self.grouper.result_ilocs())
        result = result.set_axis(original_positions, axis=self.axis, copy=False)
        result = result.sort_index(axis=self.axis)
        if self.grouper.has_dropped_na:
            # Add back in any missing rows due to dropna - index here is integral
            # with values referring to the row of the input so can use RangeIndex
            result = result.reindex(RangeIndex(len(obj_axis)), axis=self.axis)
        result = result.set_axis(obj_axis, axis=self.axis, copy=False)

        return result

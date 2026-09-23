    @final
    def _wrap_transform_fast_result(self, result: NDFrameT) -> NDFrameT:
        """
        Fast transform path for aggregations.
        """
        obj = self._obj_with_exclusions

        # for each col, reshape to size of original frame by take operation
        ids, _, _ = self.grouper.group_info
        result = result.reindex(self.grouper.result_index, axis=self.axis, copy=False)

        if self.obj.ndim == 1:
            # i.e. SeriesGroupBy
            out = algorithms.take_nd(result._values, ids)
            output = obj._constructor(out, index=obj.index, name=obj.name)
        else:
            # GH#46209
            # Don't convert indices: negative indices need to give rise
            # to null values in the result
            output = result._take(ids, axis=self.axis, convert_indices=False)
            output = output.set_axis(obj._get_axis(self.axis), axis=self.axis)
        return output

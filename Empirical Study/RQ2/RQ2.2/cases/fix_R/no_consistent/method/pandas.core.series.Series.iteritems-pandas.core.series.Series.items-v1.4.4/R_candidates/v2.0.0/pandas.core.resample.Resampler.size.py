    @doc(GroupBy.size)
    def size(self):
        result = self._downsample("size")

        # If the result is a non-empty DataFrame we stack to get a Series
        # GH 46826
        if isinstance(result, ABCDataFrame) and not result.empty:
            result = result.stack()

        if not len(self.ax):
            from pandas import Series

            if self._selected_obj.ndim == 1:
                name = self._selected_obj.name
            else:
                name = None
            result = Series([], index=result.index, dtype="int64", name=name)
        return result

    @Appender(GroupBy.size.__doc__)
    def size(self):
        result = self._downsample("size")
        if not len(self.ax):
            from pandas import Series

            if self._selected_obj.ndim == 1:
                name = self._selected_obj.name
            else:
                name = None
            result = Series([], index=result.index, dtype="int64", name=name)
        return result

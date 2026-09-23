    @Appender(GroupBy.size.__doc__)
    def size(self):
        # It's a special case as higher level does return
        # a copy of 0-len objects. GH14962
        result = self._downsample("size")
        if not len(self.ax) and isinstance(self._selected_obj, ABCDataFrame):
            result = pd.Series([], index=result.index, dtype="int64")
        return result

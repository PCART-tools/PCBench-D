    def _aggregate_item_by_item(self, func, *args, **kwargs):
        obj = self._obj_with_exclusions
        result = {}

        if self.axis > 0:
            for item in obj:
                try:
                    itemg = DataFrameGroupBy(obj[item],
                                             axis=self.axis - 1,
                                             grouper=self.grouper)
                    result[item] = itemg.aggregate(func, *args, **kwargs)
                except (ValueError, TypeError):
                    raise
            new_axes = list(obj.axes)
            new_axes[self.axis] = self.grouper.result_index
            return Panel._from_axes(result, new_axes)
        else:
            raise ValueError("axis value must be greater than 0")

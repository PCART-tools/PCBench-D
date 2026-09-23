    def _groupby_and_aggregate(self, how, grouper=None, *args, **kwargs):
        """
        Re-evaluate the obj with a groupby aggregation.
        """

        if grouper is None:
            self._set_binner()
            grouper = self.grouper

        obj = self._selected_obj

        grouped = groupby(obj, by=None, grouper=grouper, axis=self.axis)

        try:
            if isinstance(obj, ABCDataFrame) and callable(how):
                # Check if the function is reducing or not.
                result = grouped._aggregate_item_by_item(how, *args, **kwargs)
            else:
                result = grouped.aggregate(how, *args, **kwargs)
        except Exception:

            # we have a non-reducing function
            # try to evaluate
            result = grouped.apply(how, *args, **kwargs)

        result = self._apply_loffset(result)
        return self._wrap_result(result)

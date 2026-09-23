    @final
    def ohlc(self) -> DataFrame:
        """
        Compute open, high, low and close values of a group, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex

        Returns
        -------
        DataFrame
            Open, high, low and close values within each group.
        """
        if self.obj.ndim == 1:
            # self._iterate_slices() yields only self._selected_obj
            obj = self._selected_obj

            is_numeric = is_numeric_dtype(obj.dtype)
            if not is_numeric:
                raise DataError("No numeric types to aggregate")

            res_values = self.grouper._cython_operation(
                "aggregate", obj._values, "ohlc", axis=0, min_count=-1
            )

            agg_names = ["open", "high", "low", "close"]
            result = self.obj._constructor_expanddim(
                res_values, index=self.grouper.result_index, columns=agg_names
            )
            return self._reindex_output(result)

        result = self._apply_to_column_groupbys(
            lambda x: x.ohlc(), self._obj_with_exclusions
        )
        if not self.as_index:
            result = self._insert_inaxis_grouper(result)
            result.index = default_index(len(result))
        return result

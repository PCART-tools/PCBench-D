    def apply_standard(self):

        # try to reduce first (by default)
        # this only matters if the reduction in values is of different dtype
        # e.g. if we want to apply to a SparseFrame, then can't directly reduce

        # we cannot reduce using non-numpy dtypes,
        # as demonstrated in gh-12244
        if (
            self.result_type in ["reduce", None]
            and not self.dtypes.apply(is_extension_type).any()
        ):

            # Create a dummy Series from an empty array
            from pandas import Series

            values = self.values
            index = self.obj._get_axis(self.axis)
            labels = self.agg_axis
            empty_arr = np.empty(len(index), dtype=values.dtype)
            dummy = Series(empty_arr, index=index, dtype=values.dtype)

            try:
                result = reduction.reduce(
                    values, self.f, axis=self.axis, dummy=dummy, labels=labels
                )
                return self.obj._constructor_sliced(result, index=labels)
            except Exception:
                pass

        # compute the result using the series generator
        self.apply_series_generator()

        # wrap results
        return self.wrap_results()

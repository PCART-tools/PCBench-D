    def agg_series(self, obj: Series, func):
        # Caller is responsible for checking ngroups != 0
        assert self.ngroups != 0
        assert len(self.bins) > 0  # otherwise we'd get IndexError in get_result

        if is_extension_array_dtype(obj.dtype):
            # pre-empt SeriesBinGrouper from raising TypeError
            return self._aggregate_series_pure_python(obj, func)

        dummy = obj[:0]
        grouper = libreduction.SeriesBinGrouper(obj, func, self.bins, dummy)
        return grouper.get_result()

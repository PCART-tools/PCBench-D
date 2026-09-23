    def _cython_agg_general(self, how, alt=None, numeric_only=True,
                            min_count=-1):
        output = {}
        for name, obj in self._iterate_slices():
            is_numeric = is_numeric_dtype(obj.dtype)
            if numeric_only and not is_numeric:
                continue

            try:
                result, names = self.grouper.aggregate(obj.values, how,
                                                       min_count=min_count)
            except AssertionError as e:
                raise GroupByError(str(e))
            output[name] = self._try_cast(result, obj)

        if len(output) == 0:
            raise DataError('No numeric types to aggregate')

        return self._wrap_aggregated_output(output, names)

    def _cython_transform(self, how, numeric_only=True):
        output = {}
        for name, obj in self._iterate_slices():
            is_numeric = is_numeric_dtype(obj.dtype)
            if numeric_only and not is_numeric:
                continue

            try:
                result, names = self.grouper.transform(obj.values, how)
            except AssertionError as e:
                raise GroupByError(str(e))
            output[name] = self._try_cast(result, obj)

        if len(output) == 0:
            raise DataError('No numeric types to aggregate')

        return self._wrap_transformed_output(output, names)

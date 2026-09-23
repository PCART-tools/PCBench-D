    def _cython_transform(self, how: str, numeric_only: bool = True, **kwargs):
        output: Dict[base.OutputKey, np.ndarray] = {}
        for idx, obj in enumerate(self._iterate_slices()):
            name = obj.name
            is_numeric = is_numeric_dtype(obj.dtype)
            if numeric_only and not is_numeric:
                continue

            try:
                result, _ = self.grouper.transform(obj.values, how, **kwargs)
            except NotImplementedError:
                continue

            if self._transform_should_cast(how):
                result = self._try_cast(result, obj)

            key = base.OutputKey(label=name, position=idx)
            output[key] = result

        if len(output) == 0:
            raise DataError("No numeric types to aggregate")

        return self._wrap_transformed_output(output)

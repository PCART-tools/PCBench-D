    def _python_agg_general(self, func, *args, **kwargs):
        func = self._is_builtin_func(func)
        f = lambda x: func(x, *args, **kwargs)

        # iterate through "columns" ex exclusions to populate output dict
        output = {}
        for name, obj in self._iterate_slices():
            try:
                result, counts = self.grouper.agg_series(obj, f)
                output[name] = self._try_cast(result, obj, numeric_only=True)
            except TypeError:
                continue

        if len(output) == 0:
            return self._python_apply_general(f)

        if self.grouper._filter_empty_groups:

            mask = counts.ravel() > 0
            for name, result in compat.iteritems(output):

                # since we are masking, make sure that we have a float object
                values = result
                if is_numeric_dtype(values.dtype):
                    values = ensure_float(values)

                output[name] = self._try_cast(values[mask], result)

        return self._wrap_aggregated_output(output)

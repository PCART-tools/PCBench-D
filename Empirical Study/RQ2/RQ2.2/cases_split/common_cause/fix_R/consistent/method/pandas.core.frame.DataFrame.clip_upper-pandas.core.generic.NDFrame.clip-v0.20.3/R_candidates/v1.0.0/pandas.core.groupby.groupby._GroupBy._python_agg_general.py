    def _python_agg_general(self, func, *args, **kwargs):
        func = self._is_builtin_func(func)
        f = lambda x: func(x, *args, **kwargs)

        # iterate through "columns" ex exclusions to populate output dict
        output: Dict[base.OutputKey, np.ndarray] = {}

        for idx, obj in enumerate(self._iterate_slices()):
            name = obj.name
            if self.grouper.ngroups == 0:
                # agg_series below assumes ngroups > 0
                continue

            try:
                # if this function is invalid for this dtype, we will ignore it.
                func(obj[:0])
            except TypeError:
                continue
            except AssertionError:
                raise
            except Exception:
                # Our function depends on having a non-empty argument
                #  See test_groupby_agg_err_catching
                pass

            result, counts = self.grouper.agg_series(obj, f)
            assert result is not None
            key = base.OutputKey(label=name, position=idx)
            output[key] = self._try_cast(result, obj, numeric_only=True)

        if len(output) == 0:
            return self._python_apply_general(f)

        if self.grouper._filter_empty_groups:

            mask = counts.ravel() > 0
            for key, result in output.items():

                # since we are masking, make sure that we have a float object
                values = result
                if is_numeric_dtype(values.dtype):
                    values = ensure_float(values)

                output[key] = self._try_cast(values[mask], result)

        return self._wrap_aggregated_output(output)

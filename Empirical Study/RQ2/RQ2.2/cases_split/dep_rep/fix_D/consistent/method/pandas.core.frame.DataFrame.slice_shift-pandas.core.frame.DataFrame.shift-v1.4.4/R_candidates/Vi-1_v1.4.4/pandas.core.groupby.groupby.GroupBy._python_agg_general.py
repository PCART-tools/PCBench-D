    @final
    def _python_agg_general(self, func, *args, **kwargs):
        func = com.is_builtin_func(func)
        f = lambda x: func(x, *args, **kwargs)

        # iterate through "columns" ex exclusions to populate output dict
        output: dict[base.OutputKey, ArrayLike] = {}

        if self.ngroups == 0:
            # agg_series below assumes ngroups > 0
            return self._python_apply_general(f, self._selected_obj)

        for idx, obj in enumerate(self._iterate_slices()):
            name = obj.name

            try:
                # if this function is invalid for this dtype, we will ignore it.
                result = self.grouper.agg_series(obj, f)
            except TypeError:
                warn_dropping_nuisance_columns_deprecated(type(self), "agg")
                continue

            key = base.OutputKey(label=name, position=idx)
            output[key] = result

        if not output:
            return self._python_apply_general(f, self._selected_obj)

        return self._wrap_aggregated_output(output)

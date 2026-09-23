    def _python_agg_general(self, func, *args, **kwargs):
        func = com.is_builtin_func(func)
        f = lambda x: func(x, *args, **kwargs)

        # iterate through "columns" ex exclusions to populate output dict
        output: dict[base.OutputKey, ArrayLike] = {}

        if self.ngroups == 0:
            # e.g. test_evaluate_with_empty_groups different path gets different
            #  result dtype in empty case.
            return self._python_apply_general(f, self._selected_obj, is_agg=True)

        for idx, obj in enumerate(self._iterate_slices()):
            name = obj.name
            result = self.grouper.agg_series(obj, f)
            key = base.OutputKey(label=name, position=idx)
            output[key] = result

        if not output:
            # e.g. test_margins_no_values_no_cols
            return self._python_apply_general(f, self._selected_obj)

        res = self._indexed_output_to_ndframe(output)
        return self._wrap_aggregated_output(res)

    def _python_agg_general(self, func, *args, **kwargs):
        orig_func = func
        func = com.is_builtin_func(func)
        if orig_func != func:
            alias = com._builtin_table_alias[func]
            warn_alias_replacement(self, orig_func, alias)
        f = lambda x: func(x, *args, **kwargs)

        if self.ngroups == 0:
            # e.g. test_evaluate_with_empty_groups different path gets different
            #  result dtype in empty case.
            return self._python_apply_general(f, self._selected_obj, is_agg=True)

        obj = self._obj_with_exclusions
        if self.axis == 1:
            obj = obj.T

        if not len(obj.columns):
            # e.g. test_margins_no_values_no_cols
            return self._python_apply_general(f, self._selected_obj)

        output: dict[int, ArrayLike] = {}
        for idx, (name, ser) in enumerate(obj.items()):
            result = self.grouper.agg_series(ser, f)
            output[idx] = result

        res = self.obj._constructor(output)
        res.columns = obj.columns.copy(deep=False)
        return self._wrap_aggregated_output(res)

    def _python_agg_general(self, func, *args, **kwargs):
        orig_func = func
        func = com.is_builtin_func(func)
        if orig_func != func:
            alias = com._builtin_table_alias[func]
            warn_alias_replacement(self, orig_func, alias)
        f = lambda x: func(x, *args, **kwargs)

        obj = self._obj_with_exclusions
        result = self.grouper.agg_series(obj, f)
        res = obj._constructor(result, name=obj.name)
        return self._wrap_aggregated_output(res)

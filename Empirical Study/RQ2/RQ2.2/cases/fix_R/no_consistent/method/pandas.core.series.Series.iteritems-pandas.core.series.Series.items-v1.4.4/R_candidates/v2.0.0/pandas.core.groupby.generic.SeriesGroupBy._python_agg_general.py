    def _python_agg_general(self, func, *args, **kwargs):
        func = com.is_builtin_func(func)
        f = lambda x: func(x, *args, **kwargs)

        obj = self._obj_with_exclusions
        result = self.grouper.agg_series(obj, f)
        res = obj._constructor(result, name=obj.name)
        return self._wrap_aggregated_output(res)

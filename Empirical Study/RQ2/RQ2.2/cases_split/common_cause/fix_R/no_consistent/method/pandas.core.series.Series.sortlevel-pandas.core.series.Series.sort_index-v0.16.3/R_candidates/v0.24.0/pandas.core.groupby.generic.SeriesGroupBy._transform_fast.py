    def _transform_fast(self, func, func_nm):
        """
        fast version of transform, only applicable to
        builtin/cythonizable functions
        """
        if isinstance(func, compat.string_types):
            func = getattr(self, func)

        ids, _, ngroup = self.grouper.group_info
        cast = self._transform_should_cast(func_nm)
        out = algorithms.take_1d(func().values, ids)
        if cast:
            out = self._try_cast(out, self.obj)
        return Series(out, index=self.obj.index, name=self.obj.name)

    def _transform_fast(self, func):
        """
        fast version of transform, only applicable to builtin/cythonizable functions
        """
        if isinstance(func, compat.string_types):
            func = getattr(self,func)
        values = func().values
        counts = self.count().values
        values = np.repeat(values, com._ensure_platform_int(counts))

        return self._set_result_index_ordered(Series(values))

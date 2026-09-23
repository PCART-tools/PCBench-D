    def _transform_fast(self, func):
        """
        fast version of transform, only applicable to builtin/cythonizable functions
        """
        if isinstance(func, compat.string_types):
            func = getattr(self,func)

        values = func().values
        counts = self.size().fillna(0).values
        values = np.repeat(values, com._ensure_platform_int(counts))
        if any(counts == 0):
            values = self._try_cast(values, self._selected_obj)

        return self._set_result_index_ordered(Series(values))

    def _apply(self, f, **kwargs):
        """
        dispatch to _upsample; we are stripping all of the _upsample kwargs and
        performing the original function call on the grouped object
        """

        def func(x):
            x = self._shallow_copy(x, groupby=self.groupby)

            if isinstance(f, compat.string_types):
                return getattr(x, f)(**kwargs)

            return x.apply(f, **kwargs)

        result = self._groupby.apply(func)
        return self._wrap_result(result)

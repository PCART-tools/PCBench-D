    def apply_compat(self):
        """compat apply method for funcs in listlikes and dictlikes.

         Used for each callable when giving listlikes and dictlikes of callables to
         apply. Needed for compatibility with Pandas < v2.1.

        .. versionadded:: 2.1.0
        """
        obj = self.obj
        func = self.func

        if callable(func):
            f = com.get_cython_func(func)
            if f and not self.args and not self.kwargs:
                return obj.apply(func, by_row=False)

        try:
            result = obj.apply(func, by_row="compat")
        except (ValueError, AttributeError, TypeError):
            result = obj.apply(func, by_row=False)
        return result

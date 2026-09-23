    def apply(self, func, raw=None, args=(), kwargs={}):
        from pandas import Series

        kwargs.pop("_level", None)
        window = self._get_window()
        offset = _offset(window, self.center)
        index_as_array = self._get_index()

        # TODO: default is for backward compat
        # change to False in the future
        if raw is None:
            warnings.warn(
                "Currently, 'apply' passes the values as ndarrays to the "
                "applied function. In the future, this will change to passing "
                "it as Series objects. You need to specify 'raw=True' to keep "
                "the current behaviour, and you can pass 'raw=False' to "
                "silence this warning",
                FutureWarning,
                stacklevel=3,
            )
            raw = True

        def f(arg, window, min_periods, closed):
            minp = _use_window(min_periods, window)
            if not raw:
                arg = Series(arg, index=self.obj.index)
            return libwindow.roll_generic(
                arg,
                window,
                minp,
                index_as_array,
                closed,
                offset,
                func,
                raw,
                args,
                kwargs,
            )

        return self._apply(f, func, args=args, kwargs=kwargs, center=False, raw=raw)

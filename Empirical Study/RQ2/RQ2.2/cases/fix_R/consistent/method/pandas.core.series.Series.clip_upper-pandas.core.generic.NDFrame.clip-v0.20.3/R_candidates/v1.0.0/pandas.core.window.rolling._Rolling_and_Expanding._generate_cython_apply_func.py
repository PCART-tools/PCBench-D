    def _generate_cython_apply_func(self, args, kwargs, raw, offset, func):
        from pandas import Series

        window_func = partial(
            self._get_cython_func_type("roll_generic"),
            args=args,
            kwargs=kwargs,
            raw=raw,
            offset=offset,
            func=func,
        )

        def apply_func(values, begin, end, min_periods, raw=raw):
            if not raw:
                values = Series(values, index=self.obj.index)
            return window_func(values, begin, end, min_periods)

        return apply_func

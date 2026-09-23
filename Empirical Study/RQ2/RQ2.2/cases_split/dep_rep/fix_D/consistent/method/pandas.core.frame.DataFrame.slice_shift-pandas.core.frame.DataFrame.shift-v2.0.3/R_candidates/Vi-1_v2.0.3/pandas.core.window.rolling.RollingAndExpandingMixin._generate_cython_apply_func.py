    def _generate_cython_apply_func(
        self,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        raw: bool,
        function: Callable[..., Any],
    ) -> Callable[[np.ndarray, np.ndarray, np.ndarray, int], np.ndarray]:
        from pandas import Series

        window_func = partial(
            window_aggregations.roll_apply,
            args=args,
            kwargs=kwargs,
            raw=raw,
            function=function,
        )

        def apply_func(values, begin, end, min_periods, raw=raw):
            if not raw:
                # GH 45912
                values = Series(values, index=self._on, copy=False)
            return window_func(values, begin, end, min_periods)

        return apply_func

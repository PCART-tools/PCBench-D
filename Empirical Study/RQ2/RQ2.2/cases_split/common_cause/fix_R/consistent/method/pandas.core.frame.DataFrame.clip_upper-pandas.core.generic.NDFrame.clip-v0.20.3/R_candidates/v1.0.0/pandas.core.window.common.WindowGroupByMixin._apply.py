    def _apply(
        self,
        func: Callable,
        center: bool,
        require_min_periods: int = 0,
        floor: int = 1,
        is_weighted: bool = False,
        name: Optional[str] = None,
        use_numba_cache: bool = False,
        **kwargs,
    ):
        """
        Dispatch to apply; we are stripping all of the _apply kwargs and
        performing the original function call on the grouped object.
        """
        kwargs.pop("floor", None)

        # TODO: can we de-duplicate with _dispatch?
        def f(x, name=name, *args):
            x = self._shallow_copy(x)

            if isinstance(name, str):
                return getattr(x, name)(*args, **kwargs)

            return x.apply(name, *args, **kwargs)

        return self._groupby.apply(f)

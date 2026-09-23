    def _apply(
        self, func, name=None, window=None, center=None, check_minp=None, **kwargs
    ):
        """
        Dispatch to apply; we are stripping all of the _apply kwargs and
        performing the original function call on the grouped object.
        """

        def f(x, name=name, *args):
            x = self._shallow_copy(x)

            if isinstance(name, str):
                return getattr(x, name)(*args, **kwargs)

            return x.apply(name, *args, **kwargs)

        return self._groupby.apply(f)

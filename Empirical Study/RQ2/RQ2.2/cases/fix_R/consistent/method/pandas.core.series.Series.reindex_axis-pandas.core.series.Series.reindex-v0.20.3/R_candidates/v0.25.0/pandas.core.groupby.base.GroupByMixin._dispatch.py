    @staticmethod
    def _dispatch(name, *args, **kwargs):
        """
        Dispatch to apply.
        """

        def outer(self, *args, **kwargs):
            def f(x):
                x = self._shallow_copy(x, groupby=self._groupby)
                return getattr(x, name)(*args, **kwargs)

            return self._groupby.apply(f)

        outer.__name__ = name
        return outer

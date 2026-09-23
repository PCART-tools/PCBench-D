    def _reduce(
        self, op, name, axis=0, skipna=True, numeric_only=None, filter_type=None, **kwds
    ):
        """ perform the reduction type operation if we can """
        func = getattr(self, name, None)
        if func is None:
            raise TypeError(
                f"{type(self).__name__} cannot perform the operation {name}"
            )
        return func(skipna=skipna, **kwds)

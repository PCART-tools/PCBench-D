    def _reduce(self, name, skipna=True, **kwargs):
        method = getattr(self, name, None)

        if method is None:
            raise TypeError("cannot perform {name} with type {dtype}".format(
                name=name, dtype=self.dtype))

        if skipna:
            arr = self
        else:
            arr = self.dropna()

        # we don't support these kwargs.
        # They should only be present when called via pandas, so do it here.
        # instead of in `any` / `all` (which will raise if they're present,
        # thanks to nv.validate
        kwargs.pop('filter_type', None)
        kwargs.pop('numeric_only', None)
        kwargs.pop('op', None)
        return getattr(arr, name)(**kwargs)

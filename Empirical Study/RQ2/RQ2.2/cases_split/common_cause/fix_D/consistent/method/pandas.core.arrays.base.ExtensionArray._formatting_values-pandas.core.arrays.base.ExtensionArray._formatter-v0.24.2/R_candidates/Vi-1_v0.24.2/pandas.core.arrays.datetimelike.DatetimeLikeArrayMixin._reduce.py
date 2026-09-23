    def _reduce(self, name, axis=0, skipna=True, **kwargs):
        op = getattr(self, name, None)
        if op:
            return op(axis=axis, skipna=skipna, **kwargs)
        else:
            return super(DatetimeLikeArrayMixin, self)._reduce(
                name, skipna, **kwargs
            )

    def _reduce(self, name, axis=0, skipna=True, **kwargs):
        op = getattr(self, name, None)
        if op:
            return op(skipna=skipna, **kwargs)
        else:
            return super()._reduce(name, skipna, **kwargs)

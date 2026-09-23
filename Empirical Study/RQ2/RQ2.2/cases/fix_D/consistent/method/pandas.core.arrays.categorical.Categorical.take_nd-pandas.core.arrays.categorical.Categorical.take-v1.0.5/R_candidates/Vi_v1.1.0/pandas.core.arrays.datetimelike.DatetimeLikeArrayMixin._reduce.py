    def _reduce(self, name: str, skipna: bool = True, **kwargs):
        op = getattr(self, name, None)
        if op:
            return op(skipna=skipna, **kwargs)
        else:
            return super()._reduce(name, skipna, **kwargs)

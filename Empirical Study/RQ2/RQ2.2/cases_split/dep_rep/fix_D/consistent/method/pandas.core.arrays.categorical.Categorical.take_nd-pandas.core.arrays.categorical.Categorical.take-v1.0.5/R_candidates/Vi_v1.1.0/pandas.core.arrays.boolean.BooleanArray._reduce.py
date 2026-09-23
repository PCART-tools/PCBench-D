    def _reduce(self, name: str, skipna: bool = True, **kwargs):

        if name in {"any", "all"}:
            return getattr(self, name)(skipna=skipna, **kwargs)

        return super()._reduce(name, skipna, **kwargs)

    def _reduce(self, name: str, *, skipna: bool = True, **kwargs):
        method = getattr(self, name, None)

        if method is None:
            raise TypeError(f"cannot perform {name} with type {self.dtype}")

        if skipna:
            arr = self
        else:
            arr = self.dropna()

        return getattr(arr, name)(**kwargs)

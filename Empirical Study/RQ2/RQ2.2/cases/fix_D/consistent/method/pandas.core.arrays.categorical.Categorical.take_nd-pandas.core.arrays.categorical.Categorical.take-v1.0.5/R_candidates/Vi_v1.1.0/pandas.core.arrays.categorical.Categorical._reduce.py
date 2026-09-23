    def _reduce(self, name: str, skipna: bool = True, **kwargs):
        func = getattr(self, name, None)
        if func is None:
            raise TypeError(f"Categorical cannot perform the operation {name}")
        return func(skipna=skipna, **kwargs)

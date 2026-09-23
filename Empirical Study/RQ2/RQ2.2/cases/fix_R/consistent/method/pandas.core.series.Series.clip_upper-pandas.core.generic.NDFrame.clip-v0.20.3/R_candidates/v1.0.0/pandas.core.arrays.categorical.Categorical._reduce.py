    def _reduce(self, name, axis=0, **kwargs):
        func = getattr(self, name, None)
        if func is None:
            raise TypeError(f"Categorical cannot perform the operation {name}")
        return func(**kwargs)

    def apply(self, func, **kwargs) -> Self:  # type: ignore[override]
        if callable(func):
            new_array = func(self.array, **kwargs)
        else:
            new_array = getattr(self.array, func)(**kwargs)
        return type(self)([new_array], self._axes)

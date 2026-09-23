    def _accumulate(self, name: str, *, skipna: bool = True, **kwargs) -> Self:
        if name not in {"cummin", "cummax"}:
            raise TypeError(f"Accumulation {name} not supported for {type(self)}")

        op = getattr(datetimelike_accumulations, name)
        result = op(self.copy(), skipna=skipna, **kwargs)

        return type(self)._simple_new(result, dtype=self.dtype)

    def _reduce(
        self, name: str, *, skipna: bool = True, axis: AxisInt | None = 0, **kwargs
    ):
        if name in ["min", "max"]:
            return getattr(self, name)(skipna=skipna, axis=axis)

        raise TypeError(f"Cannot perform reduction '{name}' with string dtype")

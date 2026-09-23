    @property
    def _constructor(self) -> Callable[..., MultiIndex]:  # type: ignore[override]
        return type(self).from_tuples

    @property
    def _constructor(self) -> Callable[..., MultiIndex]:
        return type(self).from_tuples

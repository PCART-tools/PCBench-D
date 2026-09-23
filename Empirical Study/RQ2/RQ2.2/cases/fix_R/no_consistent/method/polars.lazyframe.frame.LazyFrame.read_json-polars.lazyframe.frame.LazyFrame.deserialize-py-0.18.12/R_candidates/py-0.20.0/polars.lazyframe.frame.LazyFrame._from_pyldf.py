    @classmethod
    def _from_pyldf(cls, ldf: PyLazyFrame) -> Self:
        self = cls.__new__(cls)
        self._ldf = ldf
        return self

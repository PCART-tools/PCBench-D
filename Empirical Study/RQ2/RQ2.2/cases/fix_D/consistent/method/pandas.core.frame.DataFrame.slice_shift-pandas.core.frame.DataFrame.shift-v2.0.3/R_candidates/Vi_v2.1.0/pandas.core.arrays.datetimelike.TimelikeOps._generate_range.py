    @classmethod
    def _generate_range(cls, start, end, periods, freq, *args, **kwargs) -> Self:
        raise AbstractMethodError(cls)

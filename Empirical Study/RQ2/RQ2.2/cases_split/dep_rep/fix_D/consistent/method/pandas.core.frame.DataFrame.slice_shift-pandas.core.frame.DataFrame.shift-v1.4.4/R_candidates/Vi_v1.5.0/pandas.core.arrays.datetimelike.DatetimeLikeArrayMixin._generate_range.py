    @classmethod
    def _generate_range(
        cls: type[DatetimeLikeArrayT], start, end, periods, freq, *args, **kwargs
    ) -> DatetimeLikeArrayT:
        raise AbstractMethodError(cls)

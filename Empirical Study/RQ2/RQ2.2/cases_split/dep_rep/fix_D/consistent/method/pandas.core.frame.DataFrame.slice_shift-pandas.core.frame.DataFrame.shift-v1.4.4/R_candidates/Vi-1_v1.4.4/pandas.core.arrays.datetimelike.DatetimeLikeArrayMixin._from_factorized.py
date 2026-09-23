    @classmethod
    def _from_factorized(
        cls: type[DatetimeLikeArrayT], values, original: DatetimeLikeArrayT
    ) -> DatetimeLikeArrayT:
        return cls(values, dtype=original.dtype)

    @classmethod
    def _from_factorized(cls, uniques, original):
        return original._constructor(
            original.categories.take(uniques), dtype=original.dtype
        )

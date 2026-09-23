    @classmethod
    def _from_factorized(cls, uniques, original):
        return original._constructor(original.categories.take(uniques),
                                     categories=original.categories,
                                     ordered=original.ordered)

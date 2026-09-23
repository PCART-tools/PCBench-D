    def value_counts(self, dropna: bool = True):
        from pandas import Series

        result = super().value_counts(dropna)
        return Series(
            result._values.to_numpy(), index=result.index, name=result.name, copy=False
        )

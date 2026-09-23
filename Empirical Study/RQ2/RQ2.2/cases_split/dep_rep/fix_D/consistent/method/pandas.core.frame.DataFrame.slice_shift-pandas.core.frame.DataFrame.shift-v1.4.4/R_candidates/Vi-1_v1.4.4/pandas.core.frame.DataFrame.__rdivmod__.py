    def __rdivmod__(self, other) -> tuple[DataFrame, DataFrame]:
        # Naive implementation, room for optimization
        div = other // self
        mod = other - div * self
        return div, mod

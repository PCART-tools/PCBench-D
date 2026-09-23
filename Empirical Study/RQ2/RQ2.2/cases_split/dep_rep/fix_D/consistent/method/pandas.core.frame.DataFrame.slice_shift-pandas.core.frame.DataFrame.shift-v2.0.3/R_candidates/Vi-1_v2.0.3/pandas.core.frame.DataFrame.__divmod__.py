    def __divmod__(self, other) -> tuple[DataFrame, DataFrame]:
        # Naive implementation, room for optimization
        div = self // other
        mod = self - div * other
        return div, mod

    def __truediv__(self, other: DataFrame | Series | int | float) -> DataFrame:
        return self._div(other, floordiv=False)

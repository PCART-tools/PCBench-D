    def __rmul__(self, other: DataFrame | Series | int | float) -> Self:
        return self * other

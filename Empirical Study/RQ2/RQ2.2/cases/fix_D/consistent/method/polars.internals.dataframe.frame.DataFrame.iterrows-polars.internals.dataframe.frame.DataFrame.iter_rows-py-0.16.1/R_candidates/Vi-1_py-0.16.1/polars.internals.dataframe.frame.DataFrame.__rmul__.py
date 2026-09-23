    def __rmul__(self: DF, other: DataFrame | pli.Series | int | float) -> DF:
        return self * other

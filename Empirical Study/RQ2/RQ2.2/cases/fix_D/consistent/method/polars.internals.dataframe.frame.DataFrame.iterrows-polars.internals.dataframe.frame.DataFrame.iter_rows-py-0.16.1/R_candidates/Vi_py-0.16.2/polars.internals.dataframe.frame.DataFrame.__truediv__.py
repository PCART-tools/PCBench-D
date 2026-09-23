    def __truediv__(self: DF, other: DF | pli.Series | int | float) -> DF:
        return self._div(other, floordiv=False)

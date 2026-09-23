    def __floordiv__(self: DF, other: DF | pli.Series | int | float) -> DF:
        return self._div(other, floordiv=True)

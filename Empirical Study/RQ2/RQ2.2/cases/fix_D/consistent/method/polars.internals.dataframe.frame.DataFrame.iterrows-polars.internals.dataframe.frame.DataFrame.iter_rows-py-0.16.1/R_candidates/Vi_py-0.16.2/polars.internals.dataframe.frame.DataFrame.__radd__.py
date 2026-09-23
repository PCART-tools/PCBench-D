    def __radd__(
        self: DF, other: DataFrame | pli.Series | int | float | bool | str
    ) -> DF:
        if isinstance(other, str):
            return self.select((pli.lit(other) + pli.col("*")).keep_name())
        return self + other

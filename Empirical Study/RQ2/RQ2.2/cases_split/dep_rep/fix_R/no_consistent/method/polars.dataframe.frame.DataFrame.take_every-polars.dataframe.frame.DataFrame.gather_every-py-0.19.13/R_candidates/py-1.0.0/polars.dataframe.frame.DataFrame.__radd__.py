    def __radd__(  # type: ignore[misc]
        self, other: DataFrame | Series | int | float | bool | str
    ) -> DataFrame:
        if isinstance(other, str):
            return self.select((lit(other) + F.col("*")).name.keep())
        return self + other

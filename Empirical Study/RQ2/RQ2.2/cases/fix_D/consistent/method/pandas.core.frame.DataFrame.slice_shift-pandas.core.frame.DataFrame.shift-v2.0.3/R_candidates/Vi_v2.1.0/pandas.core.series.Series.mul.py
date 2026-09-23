    @Appender(ops.make_flex_doc("mul", "series"))
    def mul(
        self,
        other,
        level: Level | None = None,
        fill_value: float | None = None,
        axis: Axis = 0,
    ):
        return self._flex_method(
            other, operator.mul, level=level, fill_value=fill_value, axis=axis
        )

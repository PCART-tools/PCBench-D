    def shift(
        self, periods: int, axis: AxisInt = 0, fill_value: Any = None
    ) -> list[Block]:
        values = self.values
        new_values = values.shift(periods, fill_value=fill_value, axis=axis)
        return [self.make_block_same_class(new_values)]

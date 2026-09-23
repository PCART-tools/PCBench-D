    def shift(self, periods: int, fill_value) -> Self:
        if fill_value is lib.no_default:
            fill_value = None

        return self.apply_with_block("shift", periods=periods, fill_value=fill_value)

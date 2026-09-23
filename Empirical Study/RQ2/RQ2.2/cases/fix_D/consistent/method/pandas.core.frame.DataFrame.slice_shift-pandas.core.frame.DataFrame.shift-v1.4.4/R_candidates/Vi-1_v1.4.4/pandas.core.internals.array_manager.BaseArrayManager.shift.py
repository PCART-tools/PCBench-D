    def shift(self: T, periods: int, axis: int, fill_value) -> T:
        if fill_value is lib.no_default:
            fill_value = None

        if axis == 1 and self.ndim == 2:
            # TODO column-wise shift
            raise NotImplementedError

        return self.apply_with_block(
            "shift", periods=periods, axis=axis, fill_value=fill_value
        )

    def shift(self, periods: int, axis: int = 0, fill_value: Any = None) -> list[Block]:
        """shift the block by periods, possibly upcast"""
        # convert integer to float if necessary. need to do a lot more than
        # that, handle boolean etc also

        values = cast(np.ndarray, self.values)

        new_values, fill_value = maybe_upcast(values, fill_value)

        new_values = shift(new_values, periods, axis, fill_value)

        return [self.make_block(new_values)]

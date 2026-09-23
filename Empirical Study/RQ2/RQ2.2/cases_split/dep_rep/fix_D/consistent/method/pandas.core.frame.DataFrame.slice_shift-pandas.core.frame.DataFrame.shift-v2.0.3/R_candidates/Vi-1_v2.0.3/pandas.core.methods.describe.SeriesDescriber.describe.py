    def describe(self, percentiles: Sequence[float] | np.ndarray) -> Series:
        describe_func = select_describe_func(
            self.obj,
        )
        return describe_func(self.obj, percentiles)

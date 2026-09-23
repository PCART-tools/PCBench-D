    def describe(self, percentiles: Sequence[float] | np.ndarray) -> Series:
        describe_func = select_describe_func(
            self.obj,
            self.datetime_is_numeric,
        )
        return describe_func(self.obj, percentiles)

    def shrink_to_fit(self, *, in_place: bool = False) -> Series:
        """
        Shrink Series memory usage.

        Shrinks the underlying array capacity to exactly fit the actual data.
        (Note that this function does not change the Series data type).
        """
        if in_place:
            self._s.shrink_to_fit()
            return self
        else:
            series = self.clone()
            series._s.shrink_to_fit()
            return series

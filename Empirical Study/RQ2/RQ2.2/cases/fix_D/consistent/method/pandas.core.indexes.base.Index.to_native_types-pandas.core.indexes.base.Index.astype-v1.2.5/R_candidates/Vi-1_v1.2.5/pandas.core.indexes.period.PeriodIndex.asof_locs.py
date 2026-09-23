    def asof_locs(self, where: Index, mask: np.ndarray) -> np.ndarray:
        """
        where : array of timestamps
        mask : array of booleans where data is not NA
        """
        if isinstance(where, DatetimeIndex):
            where = PeriodIndex(where._values, freq=self.freq)
        elif not isinstance(where, PeriodIndex):
            raise TypeError("asof_locs `where` must be DatetimeIndex or PeriodIndex")

        return super().asof_locs(where, mask)

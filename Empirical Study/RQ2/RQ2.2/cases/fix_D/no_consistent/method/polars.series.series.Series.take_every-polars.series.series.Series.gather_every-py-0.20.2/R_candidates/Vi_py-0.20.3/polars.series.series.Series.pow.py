    def pow(self, exponent: int | float | None | Series) -> Series:
        """
        Raise to the power of the given exponent.

        Parameters
        ----------
        exponent
            The exponent. Accepts Series input.

        Examples
        --------
        >>> s = pl.Series("foo", [1, 2, 3, 4])
        >>> s.pow(3)
        shape: (4,)
        Series: 'foo' [f64]
        [
                1.0
                8.0
                27.0
                64.0
        ]

        """
        if self.dtype.is_temporal():
            raise TypeError(
                "first cast to integer before raising datelike dtypes to a power"
            )
        if _check_for_numpy(exponent) and isinstance(exponent, np.ndarray):
            exponent = Series(exponent)
        return self.to_frame().select_seq(F.col(self.name).pow(exponent)).to_series()

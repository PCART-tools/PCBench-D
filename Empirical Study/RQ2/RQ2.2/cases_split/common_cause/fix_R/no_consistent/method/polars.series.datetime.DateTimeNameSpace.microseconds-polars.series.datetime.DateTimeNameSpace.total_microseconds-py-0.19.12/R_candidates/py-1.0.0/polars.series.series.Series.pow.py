    def pow(self, exponent: int | float | Series) -> Series:
        """
        Raise to the power of the given exponent.

        If the exponent is float, the result follows the dtype of exponent.
        Otherwise, it follows dtype of base.

        Parameters
        ----------
        exponent
            The exponent. Accepts Series input.

        Examples
        --------
        Raising integers to positive integers results in integers:

        >>> s = pl.Series("foo", [1, 2, 3, 4])
        >>> s.pow(3)
        shape: (4,)
        Series: 'foo' [i64]
        [
            1
            8
            27
            64
        ]

        In order to raise integers to negative integers, you can cast either the
        base or the exponent to float:

        >>> s.pow(-3.0)
        shape: (4,)
        Series: 'foo' [f64]
        [
                1.0
                0.125
                0.037037
                0.015625
        ]
        """
        if _check_for_numpy(exponent) and isinstance(exponent, np.ndarray):
            exponent = Series(exponent)
        return self.to_frame().select_seq(F.col(self.name).pow(exponent)).to_series()

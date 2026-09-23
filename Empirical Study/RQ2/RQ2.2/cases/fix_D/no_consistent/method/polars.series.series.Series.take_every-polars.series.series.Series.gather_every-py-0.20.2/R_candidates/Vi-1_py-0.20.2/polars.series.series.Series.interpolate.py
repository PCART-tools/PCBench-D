    def interpolate(self, method: InterpolationMethod = "linear") -> Series:
        """
        Fill null values using interpolation.

        Parameters
        ----------
        method : {'linear', 'nearest'}
            Interpolation method.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, None, None, 5])
        >>> s.interpolate()
        shape: (5,)
        Series: 'a' [f64]
        [
            1.0
            2.0
            3.0
            4.0
            5.0
        ]

        """

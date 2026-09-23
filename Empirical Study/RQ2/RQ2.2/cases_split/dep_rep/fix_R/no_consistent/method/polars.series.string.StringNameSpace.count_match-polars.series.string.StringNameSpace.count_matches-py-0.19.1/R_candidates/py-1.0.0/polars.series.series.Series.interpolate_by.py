    def interpolate_by(self, by: IntoExpr) -> Series:
        """
        Fill null values using interpolation based on another column.

        Parameters
        ----------
        by
            Column to interpolate values based on.

        Examples
        --------
        Fill null values using linear interpolation.

        >>> s = pl.Series([1, None, None, 3])
        >>> by = pl.Series([1, 2, 7, 8])
        >>> s.interpolate_by(by)
        shape: (4,)
        Series: '' [f64]
        [
            1.0
            1.285714
            2.714286
            3.0
        ]
        """

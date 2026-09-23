    def to_decimal(
        self,
        inference_length: int = 100,
    ) -> Series:
        """
        Convert a String column into a Decimal column.

        This method infers the needed parameters `precision` and `scale`.

        Parameters
        ----------
        inference_length
            Number of elements to parse to determine the `precision` and `scale`

        Examples
        --------
        >>> s = pl.Series(
        ...     ["40.12", "3420.13", "120134.19", "3212.98", "12.90", "143.09", "143.9"]
        ... )
        >>> s.str.to_decimal()
        shape: (7,)
        Series: '' [decimal[*,2]]
        [
            40.12
            3420.13
            120134.19
            3212.98
            12.90
            143.09
            143.90
        ]
        """

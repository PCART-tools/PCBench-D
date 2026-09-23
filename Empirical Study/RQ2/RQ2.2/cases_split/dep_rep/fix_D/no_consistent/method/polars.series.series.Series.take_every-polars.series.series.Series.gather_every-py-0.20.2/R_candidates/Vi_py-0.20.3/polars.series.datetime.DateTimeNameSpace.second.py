    def second(self, *, fractional: bool = False) -> Series:
        """
        Extract seconds from underlying DateTime representation.

        Applies to Datetime columns.

        Returns the integer second number from 0 to 59, or a floating
        point number from 0 < 60 if `fractional=True` that includes
        any milli/micro/nanosecond component.

        Parameters
        ----------
        fractional
            Whether to include the fractional component of the second.

        Returns
        -------
        Series
            Series of data type :class:`Int8` or :class:`Float64`.

        Examples
        --------
        >>> from datetime import datetime
        >>> s = pl.Series(
        ...     "datetime",
        ...     [
        ...         datetime(2000, 1, 1, 0, 0, 0, 456789),
        ...         datetime(2000, 1, 1, 0, 0, 3, 111110),
        ...         datetime(2000, 1, 1, 0, 0, 5, 765431),
        ...     ],
        ... )
        >>> s.dt.second()
        shape: (3,)
        Series: 'datetime' [i8]
        [
                0
                3
                5
        ]
        >>> s.dt.second(fractional=True)
        shape: (3,)
        Series: 'datetime' [f64]
        [
                0.456789
                3.11111
                5.765431
        ]

        """

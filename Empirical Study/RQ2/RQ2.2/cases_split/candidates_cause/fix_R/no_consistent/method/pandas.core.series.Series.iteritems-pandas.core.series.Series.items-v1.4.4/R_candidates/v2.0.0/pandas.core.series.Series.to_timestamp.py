    def to_timestamp(
        self,
        freq=None,
        how: Literal["s", "e", "start", "end"] = "start",
        copy: bool | None = None,
    ) -> Series:
        """
        Cast to DatetimeIndex of Timestamps, at *beginning* of period.

        Parameters
        ----------
        freq : str, default frequency of PeriodIndex
            Desired frequency.
        how : {'s', 'e', 'start', 'end'}
            Convention for converting period to timestamp; start of period
            vs. end.
        copy : bool, default True
            Whether or not to return a copy.

        Returns
        -------
        Series with DatetimeIndex

        Examples
        --------
        >>> idx = pd.PeriodIndex(['2023', '2024', '2025'], freq='Y')
        >>> s1 = pd.Series([1, 2, 3], index=idx)
        >>> s1
        2023    1
        2024    2
        2025    3
        Freq: A-DEC, dtype: int64

        The resulting frequency of the Timestamps is `YearBegin`

        >>> s1 = s1.to_timestamp()
        >>> s1
        2023-01-01    1
        2024-01-01    2
        2025-01-01    3
        Freq: AS-JAN, dtype: int64

        Using `freq` which is the offset that the Timestamps will have

        >>> s2 = pd.Series([1, 2, 3], index=idx)
        >>> s2 = s2.to_timestamp(freq='M')
        >>> s2
        2023-01-31    1
        2024-01-31    2
        2025-01-31    3
        Freq: A-JAN, dtype: int64
        """
        if not isinstance(self.index, PeriodIndex):
            raise TypeError(f"unsupported Type {type(self.index).__name__}")

        new_obj = self.copy(deep=copy and not using_copy_on_write())
        new_index = self.index.to_timestamp(freq=freq, how=how)
        setattr(new_obj, "index", new_index)
        return new_obj

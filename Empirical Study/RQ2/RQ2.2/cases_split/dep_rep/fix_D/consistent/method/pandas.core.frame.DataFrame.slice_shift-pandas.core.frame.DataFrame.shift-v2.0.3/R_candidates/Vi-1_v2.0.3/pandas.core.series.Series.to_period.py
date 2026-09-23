    def to_period(self, freq: str | None = None, copy: bool | None = None) -> Series:
        """
        Convert Series from DatetimeIndex to PeriodIndex.

        Parameters
        ----------
        freq : str, default None
            Frequency associated with the PeriodIndex.
        copy : bool, default True
            Whether or not to return a copy.

        Returns
        -------
        Series
            Series with index converted to PeriodIndex.

        Examples
        --------
        >>> idx = pd.DatetimeIndex(['2023', '2024', '2025'])
        >>> s = pd.Series([1, 2, 3], index=idx)
        >>> s = s.to_period()
        >>> s
        2023    1
        2024    2
        2025    3
        Freq: A-DEC, dtype: int64

        Viewing the index

        >>> s.index
        PeriodIndex(['2023', '2024', '2025'], dtype='period[A-DEC]')
        """
        if not isinstance(self.index, DatetimeIndex):
            raise TypeError(f"unsupported Type {type(self.index).__name__}")

        new_obj = self.copy(deep=copy and not using_copy_on_write())
        new_index = self.index.to_period(freq=freq)
        setattr(new_obj, "index", new_index)
        return new_obj

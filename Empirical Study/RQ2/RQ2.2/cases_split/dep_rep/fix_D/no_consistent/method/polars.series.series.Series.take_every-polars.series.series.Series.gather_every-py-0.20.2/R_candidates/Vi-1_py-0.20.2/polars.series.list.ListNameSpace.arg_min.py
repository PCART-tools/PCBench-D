    def arg_min(self) -> Series:
        """
        Retrieve the index of the minimal value in every sublist.

        Returns
        -------
        Series
            Series of data type :class:`UInt32` or :class:`UInt64`
            (depending on compilation).

        """

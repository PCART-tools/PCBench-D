    def concat(self, other: list[Series] | Series | list[Any]) -> Series:
        """
        Concat the arrays in a Series dtype List in linear time.

        Parameters
        ----------
        other
            Columns to concat into a List Series

        """

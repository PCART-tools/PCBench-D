    def contains(self, item: float | str | bool | int | date | datetime) -> Series:
        """
        Check if sublists contain the given item.

        Parameters
        ----------
        item
            Item that will be checked for membership

        Returns
        -------
        Series
            Series of data type :class:`Boolean`.

        """

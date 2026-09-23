    def swaplevel(self, i=-2, j=-1, copy=True):
        """
        Swap levels i and j in a :class:`MultiIndex`.

        Default is to swap the two innermost levels of the index.

        Parameters
        ----------
        i, j : int, str
            Level of the indices to be swapped. Can pass level name as string.
        copy : bool, default True
            Whether to copy underlying data.

        Returns
        -------
        Series
            Series with levels swapped in MultiIndex.
        """
        new_index = self.index.swaplevel(i, j)
        return self._constructor(self._values, index=new_index, copy=copy).__finalize__(
            self
        )

    def swaplevel(self, i, j, copy=True):
        """
        Swap levels i and j in a MultiIndex

        Parameters
        ----------
        i, j : int, string (can be mixed)
            Level of index to be swapped. Can pass level name as string.

        Returns
        -------
        swapped : Series
        """
        new_index = self.index.swaplevel(i, j)
        return self._constructor(self.values, index=new_index,
                                 copy=copy).__finalize__(self)

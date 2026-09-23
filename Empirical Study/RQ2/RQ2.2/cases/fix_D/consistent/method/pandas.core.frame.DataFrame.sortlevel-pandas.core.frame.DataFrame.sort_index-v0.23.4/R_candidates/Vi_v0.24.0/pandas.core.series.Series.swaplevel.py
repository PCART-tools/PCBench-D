    def swaplevel(self, i=-2, j=-1, copy=True):
        """
        Swap levels i and j in a MultiIndex.

        Parameters
        ----------
        i, j : int, string (can be mixed)
            Level of index to be swapped. Can pass level name as string.

        Returns
        -------
        swapped : Series

        .. versionchanged:: 0.18.1

           The indexes ``i`` and ``j`` are now optional, and default to
           the two innermost levels of the index.
        """
        new_index = self.index.swaplevel(i, j)
        return self._constructor(self._values, index=new_index,
                                 copy=copy).__finalize__(self)

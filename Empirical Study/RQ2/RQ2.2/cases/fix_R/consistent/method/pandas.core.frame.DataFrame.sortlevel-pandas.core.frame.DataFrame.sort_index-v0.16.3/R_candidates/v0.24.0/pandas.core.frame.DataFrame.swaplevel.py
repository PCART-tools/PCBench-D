    def swaplevel(self, i=-2, j=-1, axis=0):
        """
        Swap levels i and j in a MultiIndex on a particular axis.

        Parameters
        ----------
        i, j : int, string (can be mixed)
            Level of index to be swapped. Can pass level name as string.

        Returns
        -------
        swapped : same type as caller (new object)

        .. versionchanged:: 0.18.1

           The indexes ``i`` and ``j`` are now optional, and default to
           the two innermost levels of the index.
        """
        result = self.copy()

        axis = self._get_axis_number(axis)
        if axis == 0:
            result.index = result.index.swaplevel(i, j)
        else:
            result.columns = result.columns.swaplevel(i, j)
        return result

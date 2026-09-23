    def swaplevel(self, i=-2, j=-1, axis=0) -> "DataFrame":
        """
        Swap levels i and j in a MultiIndex on a particular axis.

        Parameters
        ----------
        i, j : int or str
            Levels of the indices to be swapped. Can pass level name as string.

        Returns
        -------
        DataFrame
        """
        result = self.copy()

        axis = self._get_axis_number(axis)
        if axis == 0:
            result.index = result.index.swaplevel(i, j)
        else:
            result.columns = result.columns.swaplevel(i, j)
        return result

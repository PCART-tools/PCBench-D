    def reorder_levels(self, order, axis=0) -> "DataFrame":
        """
        Rearrange index levels using input order. May not drop or duplicate levels.

        Parameters
        ----------
        order : list of int or list of str
            List representing new level order. Reference level by number
            (position) or by key (label).
        axis : int
            Where to reorder levels.

        Returns
        -------
        DataFrame
        """
        axis = self._get_axis_number(axis)
        if not isinstance(self._get_axis(axis), ABCMultiIndex):  # pragma: no cover
            raise TypeError("Can only reorder levels on a hierarchical axis.")

        result = self.copy()

        if axis == 0:
            result.index = result.index.reorder_levels(order)
        else:
            result.columns = result.columns.reorder_levels(order)
        return result

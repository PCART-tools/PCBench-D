    def swaplevel(self: FrameOrSeries, i=-2, j=-1, axis=0) -> FrameOrSeries:
        """
        Swap levels i and j in a MultiIndex on a particular axis

        Parameters
        ----------
        i, j : int, str (can be mixed)
            Level of index to be swapped. Can pass level name as string.

        Returns
        -------
        swapped : same type as caller (new object)
        """
        axis = self._get_axis_number(axis)
        result = self.copy()
        labels = result._data.axes[axis]
        result._data.set_axis(axis, labels.swaplevel(i, j))
        return result

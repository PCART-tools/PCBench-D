    @final
    def swapaxes(self: NDFrameT, axis1, axis2, copy=True) -> NDFrameT:
        """
        Interchange axes and swap values axes appropriately.

        Returns
        -------
        y : same as input
        """
        i = self._get_axis_number(axis1)
        j = self._get_axis_number(axis2)

        if i == j:
            if copy:
                return self.copy()
            return self

        mapping = {i: j, j: i}

        new_axes = (self._get_axis(mapping.get(k, k)) for k in range(self._AXIS_LEN))
        new_values = self.values.swapaxes(i, j)
        if copy:
            new_values = new_values.copy()

        return self._constructor(
            new_values,
            *new_axes,
        ).__finalize__(self, method="swapaxes")

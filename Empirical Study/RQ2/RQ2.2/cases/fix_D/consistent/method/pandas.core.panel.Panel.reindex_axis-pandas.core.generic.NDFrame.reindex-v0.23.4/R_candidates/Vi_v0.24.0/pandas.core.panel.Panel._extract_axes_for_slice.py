    @staticmethod
    def _extract_axes_for_slice(self, axes):
        """
        Return the slice dictionary for these axes.
        """
        return {self._AXIS_SLICEMAP[i]: a for i, a in
                zip(self._AXIS_ORDERS[self._AXIS_LEN - len(axes):], axes)}

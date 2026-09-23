    def _center_window(self, result, window):
        """ center the result in the window """
        if self.axis > result.ndim - 1:
            raise ValueError("Requested axis is larger then no. of argument "
                             "dimensions")

        from pandas import Series, DataFrame
        offset = _offset(window, True)
        if offset > 0:
            if isinstance(result, (Series, DataFrame)):
                result = result.slice_shift(-offset, axis=self.axis)
            else:
                lead_indexer = [slice(None)] * result.ndim
                lead_indexer[self.axis] = slice(offset, None)
                result = np.copy(result[tuple(lead_indexer)])
        return result

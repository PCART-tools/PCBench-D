    def _center_window(self, result, window) -> np.ndarray:
        """
        Center the result in the window.
        """
        if self.axis > result.ndim - 1:
            raise ValueError("Requested axis is larger then no. of argument dimensions")

        offset = calculate_center_offset(window)
        if offset > 0:
            lead_indexer = [slice(None)] * result.ndim
            lead_indexer[self.axis] = slice(offset, None)
            result = np.copy(result[tuple(lead_indexer)])
        return result

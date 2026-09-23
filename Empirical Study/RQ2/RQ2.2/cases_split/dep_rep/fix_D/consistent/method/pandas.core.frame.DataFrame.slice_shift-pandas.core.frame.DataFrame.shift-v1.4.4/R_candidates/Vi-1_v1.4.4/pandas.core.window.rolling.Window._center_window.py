    def _center_window(self, result: np.ndarray, offset: int) -> np.ndarray:
        """
        Center the result in the window for weighted rolling aggregations.
        """
        if self.axis > result.ndim - 1:
            raise ValueError("Requested axis is larger then no. of argument dimensions")

        if offset > 0:
            lead_indexer = [slice(None)] * result.ndim
            lead_indexer[self.axis] = slice(offset, None)
            result = np.copy(result[tuple(lead_indexer)])
        return result

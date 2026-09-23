    def isna(self) -> np.ndarray:
        """
        Boolean NumPy array indicating if each value is missing.

        This should return a 1-D array the same length as 'self'.
        """
        # TODO: Implement .to_numpy for ChunkedArray
        return self._data.is_null().to_pandas().values

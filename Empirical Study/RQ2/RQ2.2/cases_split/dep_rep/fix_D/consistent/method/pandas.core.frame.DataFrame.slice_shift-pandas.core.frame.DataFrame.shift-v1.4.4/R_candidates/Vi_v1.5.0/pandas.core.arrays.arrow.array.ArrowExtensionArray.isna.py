    def isna(self) -> npt.NDArray[np.bool_]:
        """
        Boolean NumPy array indicating if each value is missing.

        This should return a 1-D array the same length as 'self'.
        """
        if pa_version_under2p0:
            return self._data.is_null().to_pandas().values
        else:
            return self._data.is_null().to_numpy()

    @property
    def _ndarray_values(self) -> np.ndarray:
        """
        Internal pandas method for lossy conversion to a NumPy ndarray.

        This method is not part of the pandas interface.

        The expectation is that this is cheap to compute, and is primarily
        used for interacting with our indexers.

        Returns
        -------
        array : ndarray
        """
        return np.array(self)

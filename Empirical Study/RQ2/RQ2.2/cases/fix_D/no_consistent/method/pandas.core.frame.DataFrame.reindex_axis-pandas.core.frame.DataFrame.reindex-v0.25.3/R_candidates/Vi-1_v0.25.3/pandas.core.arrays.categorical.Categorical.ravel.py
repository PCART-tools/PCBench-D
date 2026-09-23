    def ravel(self, order="C"):
        """
        Return a flattened (numpy) array.

        For internal compatibility with numpy arrays.

        Returns
        -------
        numpy.array
        """
        warn(
            "Categorical.ravel will return a Categorical object instead "
            "of an ndarray in a future version.",
            FutureWarning,
            stacklevel=2,
        )
        return np.array(self)

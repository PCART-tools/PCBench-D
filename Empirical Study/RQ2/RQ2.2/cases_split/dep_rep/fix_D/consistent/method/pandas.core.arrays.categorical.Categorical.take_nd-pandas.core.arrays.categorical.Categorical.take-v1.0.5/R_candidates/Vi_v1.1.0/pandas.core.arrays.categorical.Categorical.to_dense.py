    def to_dense(self):
        """
        Return my 'dense' representation

        For internal compatibility with numpy arrays.

        Returns
        -------
        dense : array
        """
        warn(
            "Categorical.to_dense is deprecated and will be removed in "
            "a future version.  Use np.asarray(cat) instead.",
            FutureWarning,
            stacklevel=2,
        )
        return np.asarray(self)

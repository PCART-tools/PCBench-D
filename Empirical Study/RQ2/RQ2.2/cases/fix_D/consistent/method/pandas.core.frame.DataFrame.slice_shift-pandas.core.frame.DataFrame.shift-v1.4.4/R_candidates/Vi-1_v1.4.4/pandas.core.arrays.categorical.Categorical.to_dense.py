    def to_dense(self) -> np.ndarray:
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
            stacklevel=find_stack_level(),
        )
        return np.asarray(self)

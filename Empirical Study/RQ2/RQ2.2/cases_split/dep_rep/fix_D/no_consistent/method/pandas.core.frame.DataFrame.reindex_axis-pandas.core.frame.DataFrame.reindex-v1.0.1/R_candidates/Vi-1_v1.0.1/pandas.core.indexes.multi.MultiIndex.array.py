    @property
    def array(self):
        """
        Raises a ValueError for `MultiIndex` because there's no single
        array backing a MultiIndex.

        Raises
        ------
        ValueError
        """
        raise ValueError(
            "MultiIndex has no single backing array. Use "
            "'MultiIndex.to_numpy()' to get a NumPy array of tuples."
        )

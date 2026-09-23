    @property
    def column_arrays(self) -> list[ArrayLike]:
        """
        Used in the JSON C code to access column arrays.
        """

        return [np.asarray(arr) for arr in self.arrays]

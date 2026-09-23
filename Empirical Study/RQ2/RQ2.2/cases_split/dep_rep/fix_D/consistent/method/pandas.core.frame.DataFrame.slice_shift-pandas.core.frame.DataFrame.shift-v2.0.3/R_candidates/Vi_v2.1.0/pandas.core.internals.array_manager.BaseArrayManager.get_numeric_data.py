    def get_numeric_data(self, copy: bool = False) -> Self:
        """
        Select columns that have a numeric dtype.

        Parameters
        ----------
        copy : bool, default False
            Whether to copy the blocks
        """
        return self._get_data_subset(
            lambda arr: is_numeric_dtype(arr.dtype)
            or getattr(arr.dtype, "_is_numeric", False)
        )

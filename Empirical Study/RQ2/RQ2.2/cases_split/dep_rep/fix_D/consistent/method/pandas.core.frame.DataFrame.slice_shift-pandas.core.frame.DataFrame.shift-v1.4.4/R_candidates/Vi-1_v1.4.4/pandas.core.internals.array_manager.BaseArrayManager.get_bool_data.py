    def get_bool_data(self: T, copy: bool = False) -> T:
        """
        Select columns that are bool-dtype and object-dtype columns that are all-bool.

        Parameters
        ----------
        copy : bool, default False
            Whether to copy the blocks
        """
        return self._get_data_subset(is_inferred_bool_dtype)

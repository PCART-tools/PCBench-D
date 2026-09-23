    def get_bool_data(self, copy: bool = False) -> Self:
        """
        Select columns that are bool-dtype and object-dtype columns that are all-bool.

        Parameters
        ----------
        copy : bool, default False
            Whether to copy the blocks
        """
        return self._get_data_subset(lambda x: x.dtype == np.dtype(bool))

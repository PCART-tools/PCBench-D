    def take(self, indices, axis=0, convert=True, is_copy=True):
        """
        Analogous to ndarray.take

        Parameters
        ----------
        indices : list / array of ints
        axis : int, default 0
        convert : translate neg to pos indices (default)
        is_copy : mark the returned frame as a copy

        Returns
        -------
        taken : type of caller
        """

        new_data = self._data.take(indices,
                                   axis=self._get_block_manager_axis(axis),
                                   convert=True, verify=True)
        result = self._constructor(new_data).__finalize__(self)

        # maybe set copy if we didn't actually change the index
        if is_copy and not result._get_axis(axis).equals(self._get_axis(axis)):
            result._set_is_copy(self)

        return result

    def _validate_integer(self, key, axis):
        """
        Check that 'key' is a valid position in the desired axis.

        Parameters
        ----------
        key : int
            Requested position
        axis : int
            Desired axis

        Returns
        -------
        None

        Raises
        ------
        IndexError
            If 'key' is not a valid position in axis 'axis'
        """

        len_axis = len(self.obj._get_axis(axis))
        if key >= len_axis or key < -len_axis:
            raise IndexError("single positional indexer is out-of-bounds")

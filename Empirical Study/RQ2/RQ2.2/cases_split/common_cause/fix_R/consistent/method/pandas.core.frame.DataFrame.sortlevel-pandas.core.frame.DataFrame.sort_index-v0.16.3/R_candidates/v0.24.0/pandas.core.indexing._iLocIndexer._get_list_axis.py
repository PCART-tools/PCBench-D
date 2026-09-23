    def _get_list_axis(self, key, axis=None):
        """
        Return Series values by list or array of integers

        Parameters
        ----------
        key : list-like positional indexer
        axis : int (can only be zero)

        Returns
        -------
        Series object
        """
        if axis is None:
            axis = self.axis or 0
        try:
            return self.obj._take(key, axis=axis)
        except IndexError:
            # re-raise with different error message
            raise IndexError("positional indexers are out-of-bounds")

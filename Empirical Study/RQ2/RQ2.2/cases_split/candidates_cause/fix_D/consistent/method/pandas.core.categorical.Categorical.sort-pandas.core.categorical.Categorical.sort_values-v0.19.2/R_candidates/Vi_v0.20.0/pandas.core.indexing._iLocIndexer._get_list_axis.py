    def _get_list_axis(self, key, axis=0):
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
        try:
            return self.obj.take(key, axis=axis, convert=False)
        except IndexError:
            # re-raise with different error message
            raise IndexError("positional indexers are out-of-bounds")

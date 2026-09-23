    def _get_list_axis(self, key, axis: int):
        """
        Return Series values by list or array of integers.

        Parameters
        ----------
        key : list-like positional indexer
        axis : int

        Returns
        -------
        Series object

        Notes
        -----
        `axis` can only be zero.
        """
        try:
            return self.obj._take_with_is_copy(key, axis=axis)
        except IndexError as err:
            # re-raise with different error message
            raise IndexError("positional indexers are out-of-bounds") from err

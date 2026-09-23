    def as_blocks(self, copy=True):
        """
        Convert the frame to a dict of dtype -> Constructor Types that each has
        a homogeneous dtype.

        .. deprecated:: 0.21.0

        NOTE: the dtypes of the blocks WILL BE PRESERVED HERE (unlike in
              as_matrix)

        Parameters
        ----------
        copy : boolean, default True

        Returns
        -------
        values : a dict of dtype -> Constructor Types
        """
        warnings.warn(
            "as_blocks is deprecated and will " "be removed in a future version",
            FutureWarning,
            stacklevel=2,
        )
        return self._to_dict_of_blocks(copy=copy)

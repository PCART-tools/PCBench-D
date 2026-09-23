    def reversed(self, name=None):
        """
        Make a reversed instance of the Colormap.

        .. note:: Function not implemented for base class.

        Parameters
        ----------
        name : str, optional
            The name for the reversed colormap. If it's None the
            name will be the name of the parent colormap + "_r".

        See Also
        --------
        LinearSegmentedColormap.reversed
        ListedColormap.reversed
        """
        raise NotImplementedError()

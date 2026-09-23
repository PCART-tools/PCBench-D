    def resampled(self, lutshape):
        """
        Return a new colormap with *lutshape* entries.

        Parameters
        ----------
        lutshape : tuple of (`int`, `None`)
            The tuple must have a length matching the number of variates.
            For each element in the tuple, if `int`, the corresponding colorbar
            is resampled, if `None`, the corresponding colorbar is not resampled.

        Returns
        -------
        MultivarColormap
        """

        if not np.iterable(lutshape) or len(lutshape) != len(self):
            raise ValueError(f"lutshape must be of length {len(self)}")
        new_cmap = self.copy()
        for i, s in enumerate(lutshape):
            if s is not None:
                new_cmap._colormaps[i] = self[i].resampled(s)
        return new_cmap

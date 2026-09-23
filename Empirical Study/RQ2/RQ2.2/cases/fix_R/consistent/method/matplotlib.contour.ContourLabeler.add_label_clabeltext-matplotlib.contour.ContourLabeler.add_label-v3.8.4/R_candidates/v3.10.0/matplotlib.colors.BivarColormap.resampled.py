    def resampled(self, lutshape, transposed=False):
        """
        Return a new colormap with *lutshape* entries.

        Note that this function does not move the origin.

        Parameters
        ----------
        lutshape : tuple of ints or None
            The tuple must be of length 2, and each entry is either an int or None.

            - If an int, the corresponding axis is resampled.
            - If negative the corresponding axis is resampled in reverse
            - If -1, the axis is inverted
            - If 1 or None, the corresponding axis is not resampled.

        transposed : bool, default: False
            if True, the axes are swapped after resampling

        Returns
        -------
        BivarColormap
        """

        if not np.iterable(lutshape) or len(lutshape) != 2:
            raise ValueError("lutshape must be of length 2")
        lutshape = [lutshape[0], lutshape[1]]
        if lutshape[0] is None or lutshape[0] == 1:
            lutshape[0] = self.N
        if lutshape[1] is None or lutshape[1] == 1:
            lutshape[1] = self.M

        inverted = [False, False]
        if lutshape[0] < 0:
            inverted[0] = True
            lutshape[0] = -lutshape[0]
            if lutshape[0] == 1:
                lutshape[0] = self.N
        if lutshape[1] < 0:
            inverted[1] = True
            lutshape[1] = -lutshape[1]
            if lutshape[1] == 1:
                lutshape[1] = self.M
        x_0, x_1 = np.mgrid[0:1:(lutshape[0] * 1j), 0:1:(lutshape[1] * 1j)]
        if inverted[0]:
            x_0 = x_0[::-1, :]
        if inverted[1]:
            x_1 = x_1[:, ::-1]

        # we need to use shape = 'square' while resampling the colormap.
        # if the colormap has shape = 'circle' we would otherwise get *outside* in the
        # resampled colormap
        shape_memory = self._shape
        self._shape = 'square'
        if transposed:
            new_lut = self((x_1, x_0))
            new_cmap = BivarColormapFromImage(new_lut, name=self.name,
                                              shape=shape_memory,
                                              origin=self.origin[::-1])
        else:
            new_lut = self((x_0, x_1))
            new_cmap = BivarColormapFromImage(new_lut, name=self.name,
                                              shape=shape_memory,
                                              origin=self.origin)
        self._shape = shape_memory

        new_cmap._rgba_bad = self._rgba_bad
        new_cmap._rgba_outside = self._rgba_outside
        return new_cmap

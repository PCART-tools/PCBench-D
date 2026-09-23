    def __init__(self, boundaries, ncolors, clip=False):
        """
        Parameters
        ----------
        boundaries : array-like
            Monotonically increasing sequence of boundaries
        ncolors : int
            Number of colors in the colormap to be used
        clip : bool, optional
            If clip is ``True``, out of range values are mapped to 0 if they
            are below ``boundaries[0]`` or mapped to ncolors - 1 if they are
            above ``boundaries[-1]``.

            If clip is ``False``, out of range values are mapped to -1 if
            they are below ``boundaries[0]`` or mapped to ncolors if they are
            above ``boundaries[-1]``. These are then converted to valid indices
            by :meth:`Colormap.__call__`.

        Notes
        -----
        *boundaries* defines the edges of bins, and data falling within a bin
        is mapped to the color with the same index.

        If the number of bins doesn't equal *ncolors*, the color is chosen
        by linear interpolation of the bin number onto color numbers.
        """
        self.clip = clip
        self.vmin = boundaries[0]
        self.vmax = boundaries[-1]
        self.boundaries = np.asarray(boundaries)
        self.N = len(self.boundaries)
        self.Ncmap = ncolors
        if self.N - 1 == self.Ncmap:
            self._interp = False
        else:
            self._interp = True

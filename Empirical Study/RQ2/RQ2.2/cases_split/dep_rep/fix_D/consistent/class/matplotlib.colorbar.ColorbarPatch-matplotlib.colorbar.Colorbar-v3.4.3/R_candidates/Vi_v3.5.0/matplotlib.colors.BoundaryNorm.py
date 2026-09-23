class BoundaryNorm(Normalize):
    """
    Generate a colormap index based on discrete intervals.

    Unlike `Normalize` or `LogNorm`, `BoundaryNorm` maps values to integers
    instead of to the interval 0-1.

    Mapping to the 0-1 interval could have been done via piece-wise linear
    interpolation, but using integers seems simpler, and reduces the number of
    conversions back and forth between integer and floating point.
    """
    def __init__(self, boundaries, ncolors, clip=False, *, extend='neither'):
        """
        Parameters
        ----------
        boundaries : array-like
            Monotonically increasing sequence of at least 2 boundaries.
        ncolors : int
            Number of colors in the colormap to be used.
        clip : bool, optional
            If clip is ``True``, out of range values are mapped to 0 if they
            are below ``boundaries[0]`` or mapped to ``ncolors - 1`` if they
            are above ``boundaries[-1]``.

            If clip is ``False``, out of range values are mapped to -1 if
            they are below ``boundaries[0]`` or mapped to *ncolors* if they are
            above ``boundaries[-1]``. These are then converted to valid indices
            by `Colormap.__call__`.
        extend : {'neither', 'both', 'min', 'max'}, default: 'neither'
            Extend the number of bins to include one or both of the
            regions beyond the boundaries.  For example, if ``extend``
            is 'min', then the color to which the region between the first
            pair of boundaries is mapped will be distinct from the first
            color in the colormap, and by default a
            `~matplotlib.colorbar.Colorbar` will be drawn with
            the triangle extension on the left or lower end.

        Returns
        -------
        int16 scalar or array

        Notes
        -----
        *boundaries* defines the edges of bins, and data falling within a bin
        is mapped to the color with the same index.

        If the number of bins, including any extensions, is less than
        *ncolors*, the color index is chosen by linear interpolation, mapping
        the ``[0, nbins - 1]`` range onto the ``[0, ncolors - 1]`` range.
        """
        if clip and extend != 'neither':
            raise ValueError("'clip=True' is not compatible with 'extend'")
        super().__init__(vmin=boundaries[0], vmax=boundaries[-1], clip=clip)
        self.boundaries = np.asarray(boundaries)
        self.N = len(self.boundaries)
        if self.N < 2:
            raise ValueError("You must provide at least 2 boundaries "
                             f"(1 region) but you passed in {boundaries!r}")
        self.Ncmap = ncolors
        self.extend = extend

        self._scale = None  # don't use the default scale.

        self._n_regions = self.N - 1  # number of colors needed
        self._offset = 0
        if extend in ('min', 'both'):
            self._n_regions += 1
            self._offset = 1
        if extend in ('max', 'both'):
            self._n_regions += 1
        if self._n_regions > self.Ncmap:
            raise ValueError(f"There are {self._n_regions} color bins "
                             "including extensions, but ncolors = "
                             f"{ncolors}; ncolors must equal or exceed the "
                             "number of bins")

    def __call__(self, value, clip=None):
        if clip is None:
            clip = self.clip

        xx, is_scalar = self.process_value(value)
        mask = np.ma.getmaskarray(xx)
        # Fill masked values a value above the upper boundary
        xx = np.atleast_1d(xx.filled(self.vmax + 1))
        if clip:
            np.clip(xx, self.vmin, self.vmax, out=xx)
            max_col = self.Ncmap - 1
        else:
            max_col = self.Ncmap
        # this gives us the bins in the lookup table in the range
        # [0, _n_regions - 1]  (the offset is set in the init)
        iret = np.digitize(xx, self.boundaries) - 1 + self._offset
        # if we have more colors than regions, stretch the region
        # index computed above to full range of the color bins.  This
        # will make use of the full range (but skip some of the colors
        # in the middle) such that the first region is mapped to the
        # first color and the last region is mapped to the last color.
        if self.Ncmap > self._n_regions:
            if self._n_regions == 1:
                # special case the 1 region case, pick the middle color
                iret[iret == 0] = (self.Ncmap - 1) // 2
            else:
                # otherwise linearly remap the values from the region index
                # to the color index spaces
                iret = (self.Ncmap - 1) / (self._n_regions - 1) * iret
        # cast to 16bit integers in all cases
        iret = iret.astype(np.int16)
        iret[xx < self.vmin] = -1
        iret[xx >= self.vmax] = max_col
        ret = np.ma.array(iret, mask=mask)
        if is_scalar:
            ret = int(ret[0])  # assume python scalar
        return ret

    def inverse(self, value):
        """
        Raises
        ------
        ValueError
            BoundaryNorm is not invertible, so calling this method will always
            raise an error
        """
        raise ValueError("BoundaryNorm is not invertible")

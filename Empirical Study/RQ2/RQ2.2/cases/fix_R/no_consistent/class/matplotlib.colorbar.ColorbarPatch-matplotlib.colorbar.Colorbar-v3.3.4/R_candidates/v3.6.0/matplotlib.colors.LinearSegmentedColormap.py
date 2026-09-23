class LinearSegmentedColormap(Colormap):
    """
    Colormap objects based on lookup tables using linear segments.

    The lookup table is generated using linear interpolation for each
    primary color, with the 0-1 domain divided into any number of
    segments.
    """

    def __init__(self, name, segmentdata, N=256, gamma=1.0):
        """
        Create colormap from linear mapping segments

        segmentdata argument is a dictionary with a red, green and blue
        entries. Each entry should be a list of *x*, *y0*, *y1* tuples,
        forming rows in a table. Entries for alpha are optional.

        Example: suppose you want red to increase from 0 to 1 over
        the bottom half, green to do the same over the middle half,
        and blue over the top half.  Then you would use::

            cdict = {'red':   [(0.0,  0.0, 0.0),
                               (0.5,  1.0, 1.0),
                               (1.0,  1.0, 1.0)],

                     'green': [(0.0,  0.0, 0.0),
                               (0.25, 0.0, 0.0),
                               (0.75, 1.0, 1.0),
                               (1.0,  1.0, 1.0)],

                     'blue':  [(0.0,  0.0, 0.0),
                               (0.5,  0.0, 0.0),
                               (1.0,  1.0, 1.0)]}

        Each row in the table for a given color is a sequence of
        *x*, *y0*, *y1* tuples.  In each sequence, *x* must increase
        monotonically from 0 to 1.  For any input value *z* falling
        between *x[i]* and *x[i+1]*, the output value of a given color
        will be linearly interpolated between *y1[i]* and *y0[i+1]*::

            row i:   x  y0  y1
                           /
                          /
            row i+1: x  y0  y1

        Hence y0 in the first row and y1 in the last row are never used.

        See Also
        --------
        LinearSegmentedColormap.from_list
            Static method; factory function for generating a smoothly-varying
            LinearSegmentedColormap.
        """
        # True only if all colors in map are identical; needed for contouring.
        self.monochrome = False
        super().__init__(name, N)
        self._segmentdata = segmentdata
        self._gamma = gamma

    def _init(self):
        self._lut = np.ones((self.N + 3, 4), float)
        self._lut[:-3, 0] = _create_lookup_table(
            self.N, self._segmentdata['red'], self._gamma)
        self._lut[:-3, 1] = _create_lookup_table(
            self.N, self._segmentdata['green'], self._gamma)
        self._lut[:-3, 2] = _create_lookup_table(
            self.N, self._segmentdata['blue'], self._gamma)
        if 'alpha' in self._segmentdata:
            self._lut[:-3, 3] = _create_lookup_table(
                self.N, self._segmentdata['alpha'], 1)
        self._isinit = True
        self._set_extremes()

    def set_gamma(self, gamma):
        """Set a new gamma value and regenerate colormap."""
        self._gamma = gamma
        self._init()

    @staticmethod
    def from_list(name, colors, N=256, gamma=1.0):
        """
        Create a `LinearSegmentedColormap` from a list of colors.

        Parameters
        ----------
        name : str
            The name of the colormap.
        colors : array-like of colors or array-like of (value, color)
            If only colors are given, they are equidistantly mapped from the
            range :math:`[0, 1]`; i.e. 0 maps to ``colors[0]`` and 1 maps to
            ``colors[-1]``.
            If (value, color) pairs are given, the mapping is from *value*
            to *color*. This can be used to divide the range unevenly.
        N : int
            The number of rgb quantization levels.
        gamma : float
        """
        if not np.iterable(colors):
            raise ValueError('colors must be iterable')

        if (isinstance(colors[0], Sized) and len(colors[0]) == 2
                and not isinstance(colors[0], str)):
            # List of value, color pairs
            vals, colors = zip(*colors)
        else:
            vals = np.linspace(0, 1, len(colors))

        r, g, b, a = to_rgba_array(colors).T
        cdict = {
            "red": np.column_stack([vals, r, r]),
            "green": np.column_stack([vals, g, g]),
            "blue": np.column_stack([vals, b, b]),
            "alpha": np.column_stack([vals, a, a]),
        }

        return LinearSegmentedColormap(name, cdict, N, gamma)

    def resampled(self, lutsize):
        """Return a new colormap with *lutsize* entries."""
        new_cmap = LinearSegmentedColormap(self.name, self._segmentdata,
                                           lutsize)
        new_cmap._rgba_over = self._rgba_over
        new_cmap._rgba_under = self._rgba_under
        new_cmap._rgba_bad = self._rgba_bad
        return new_cmap

    # Helper ensuring picklability of the reversed cmap.
    @staticmethod
    def _reverser(func, x):
        return func(1 - x)

    def reversed(self, name=None):
        """
        Return a reversed instance of the Colormap.

        Parameters
        ----------
        name : str, optional
            The name for the reversed colormap. If it's None the
            name will be the name of the parent colormap + "_r".

        Returns
        -------
        LinearSegmentedColormap
            The reversed colormap.
        """
        if name is None:
            name = self.name + "_r"

        # Using a partial object keeps the cmap picklable.
        data_r = {key: (functools.partial(self._reverser, data)
                        if callable(data) else
                        [(1.0 - x, y1, y0) for x, y0, y1 in reversed(data)])
                  for key, data in self._segmentdata.items()}

        new_cmap = LinearSegmentedColormap(name, data_r, self.N, self._gamma)
        # Reverse the over/under values too
        new_cmap._rgba_over = self._rgba_under
        new_cmap._rgba_under = self._rgba_over
        new_cmap._rgba_bad = self._rgba_bad
        return new_cmap

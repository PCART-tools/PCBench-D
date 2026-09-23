class ListedColormap(Colormap):
    """
    Colormap object generated from a list of colors.

    This may be most useful when indexing directly into a colormap,
    but it can also be used to generate special colormaps for ordinary
    mapping.

    Parameters
    ----------
    colors : list, array
        List of Matplotlib color specifications, or an equivalent Nx3 or Nx4
        floating point array (*N* rgb or rgba values).
    name : str, optional
        String to identify the colormap.
    N : int, optional
        Number of entries in the map. The default is *None*, in which case
        there is one colormap entry for each element in the list of colors.
        If ::

            N < len(colors)

        the list will be truncated at *N*. If ::

            N > len(colors)

        the list will be extended by repetition.
    """
    def __init__(self, colors, name='from_list', N=None):
        self.monochrome = False  # Are all colors identical? (for contour.py)
        if N is None:
            self.colors = colors
            N = len(colors)
        else:
            if isinstance(colors, str):
                self.colors = [colors] * N
                self.monochrome = True
            elif np.iterable(colors):
                if len(colors) == 1:
                    self.monochrome = True
                self.colors = list(
                    itertools.islice(itertools.cycle(colors), N))
            else:
                try:
                    gray = float(colors)
                except TypeError:
                    pass
                else:
                    self.colors = [gray] * N
                self.monochrome = True
        super().__init__(name, N)

    def _init(self):
        self._lut = np.zeros((self.N + 3, 4), float)
        self._lut[:-3] = to_rgba_array(self.colors)
        self._isinit = True
        self._set_extremes()

    def _resample(self, lutsize):
        """Return a new colormap with *lutsize* entries."""
        colors = self(np.linspace(0, 1, lutsize))
        new_cmap = ListedColormap(colors, name=self.name)
        # Keep the over/under values too
        new_cmap._rgba_over = self._rgba_over
        new_cmap._rgba_under = self._rgba_under
        new_cmap._rgba_bad = self._rgba_bad
        return new_cmap

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
        ListedColormap
            A reversed instance of the colormap.
        """
        if name is None:
            name = self.name + "_r"

        colors_r = list(reversed(self.colors))
        new_cmap = ListedColormap(colors_r, name=name, N=self.N)
        # Reverse the over/under values too
        new_cmap._rgba_over = self._rgba_under
        new_cmap._rgba_under = self._rgba_over
        new_cmap._rgba_bad = self._rgba_bad
        return new_cmap

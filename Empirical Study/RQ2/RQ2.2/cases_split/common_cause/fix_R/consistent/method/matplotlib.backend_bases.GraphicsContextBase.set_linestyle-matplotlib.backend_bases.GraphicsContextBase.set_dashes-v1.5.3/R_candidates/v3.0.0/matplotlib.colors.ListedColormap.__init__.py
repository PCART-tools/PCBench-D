    def __init__(self, colors, name='from_list', N=None):
        """
        Make a colormap from a list of colors.

        *colors*
            a list of matplotlib color specifications,
            or an equivalent Nx3 or Nx4 floating point array
            (*N* rgb or rgba values)
        *name*
            a string to identify the colormap
        *N*
            the number of entries in the map.  The default is *None*,
            in which case there is one colormap entry for each
            element in the list of colors.  If::

                N < len(colors)

            the list will be truncated at *N*.  If::

                N > len(colors)

            the list will be extended by repetition.
        """
        self.monochrome = False  # True only if all colors in map are
                                 # identical; needed for contouring.
        if N is None:
            self.colors = colors
            N = len(colors)
        else:
            if isinstance(colors, str):
                self.colors = [colors] * N
                self.monochrome = True
            elif cbook.iterable(colors):
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
        Colormap.__init__(self, name, N)

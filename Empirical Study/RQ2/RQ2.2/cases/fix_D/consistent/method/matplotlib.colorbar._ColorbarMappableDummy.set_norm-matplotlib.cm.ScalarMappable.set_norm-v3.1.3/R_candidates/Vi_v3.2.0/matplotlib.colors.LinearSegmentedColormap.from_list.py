    @staticmethod
    def from_list(name, colors, N=256, gamma=1.0):
        """
        Make a linear segmented colormap with *name* from a sequence
        of *colors* which evenly transitions from colors[0] at val=0
        to colors[-1] at val=1.  *N* is the number of rgb quantization
        levels.
        Alternatively, a list of (value, color) tuples can be given
        to divide the range unevenly.
        """

        if not np.iterable(colors):
            raise ValueError('colors must be iterable')

        if (isinstance(colors[0], Sized) and len(colors[0]) == 2
                and not isinstance(colors[0], str)):
            # List of value, color pairs
            vals, colors = zip(*colors)
        else:
            vals = np.linspace(0, 1, len(colors))

        cdict = dict(red=[], green=[], blue=[], alpha=[])
        for val, color in zip(vals, colors):
            r, g, b, a = to_rgba(color)
            cdict['red'].append((val, r, r))
            cdict['green'].append((val, g, g))
            cdict['blue'].append((val, b, b))
            cdict['alpha'].append((val, a, a))

        return LinearSegmentedColormap(name, cdict, N, gamma)

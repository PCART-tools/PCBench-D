    def __init__(self, axis, **kwargs):
        """
        Parameters
        ----------
        axis : `~matplotlib.axis.Axis`
            The axis for the scale.
        basex, basey : float, default: 10
            The base of the logarithm.
        nonposx, nonposy : {'clip', 'mask'}, default: 'clip'
            Determines the behavior for non-positive values. They can either
            be masked as invalid, or clipped to a very small positive number.
        subsx, subsy : sequence of int, default: None
            Where to place the subticks between each major tick.
            For example, in a log10 scale: ``[2, 3, 4, 5, 6, 7, 8, 9]``
            will place 8 logarithmically spaced minor ticks between
            each major tick.
        """
        if axis.axis_name == 'x':
            base = kwargs.pop('basex', 10.0)
            subs = kwargs.pop('subsx', None)
            nonpos = kwargs.pop('nonposx', 'clip')
            cbook._check_in_list(['mask', 'clip'], nonposx=nonpos)
        else:
            base = kwargs.pop('basey', 10.0)
            subs = kwargs.pop('subsy', None)
            nonpos = kwargs.pop('nonposy', 'clip')
            cbook._check_in_list(['mask', 'clip'], nonposy=nonpos)

        if kwargs:
            raise TypeError(f"LogScale got an unexpected keyword "
                            f"argument {next(iter(kwargs))!r}")

        if base <= 0 or base == 1:
            raise ValueError('The log base cannot be <= 0 or == 1')

        self._transform = LogTransform(base, nonpos)
        self.subs = subs

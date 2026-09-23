    def __init__(self, axis, **kwargs):
        """
        *basex*/*basey*:
           The base of the logarithm

        *nonposx*/*nonposy*: {'mask', 'clip'}
          non-positive values in *x* or *y* can be masked as
          invalid, or clipped to a very small positive number

        *subsx*/*subsy*:
           Where to place the subticks between each major tick.
           Should be a sequence of integers.  For example, in a log10
           scale: ``[2, 3, 4, 5, 6, 7, 8, 9]``

           will place 8 logarithmically spaced minor ticks between
           each major tick.
        """
        if axis.axis_name == 'x':
            base = kwargs.pop('basex', 10.0)
            subs = kwargs.pop('subsx', None)
            nonpos = kwargs.pop('nonposx', 'clip')
        else:
            base = kwargs.pop('basey', 10.0)
            subs = kwargs.pop('subsy', None)
            nonpos = kwargs.pop('nonposy', 'clip')

        if len(kwargs):
            raise ValueError(("provided too many kwargs, can only pass "
                              "{'basex', 'subsx', nonposx'} or "
                              "{'basey', 'subsy', nonposy'}.  You passed ") +
                             "{!r}".format(kwargs))

        if nonpos not in ['mask', 'clip']:
            raise ValueError("nonposx, nonposy kwarg must be 'mask' or 'clip'")
        if base <= 0 or base == 1:
            raise ValueError('The log base cannot be <= 0 or == 1')

        if base == 10.0:
            self._transform = self.Log10Transform(nonpos)
        elif base == 2.0:
            self._transform = self.Log2Transform(nonpos)
        elif base == np.e:
            self._transform = self.NaturalLogTransform(nonpos)
        else:
            self._transform = self.LogTransform(base, nonpos)

        self.base = base
        self.subs = subs

    def __init__(self, axis, **kwargs):
        """
        *basex*/*basey*:
           The base of the logarithm

        *linthreshx*/*linthreshy*:
          A single float which defines the range (-*x*, *x*), within
          which the plot is linear. This avoids having the plot go to
          infinity around zero.

        *subsx*/*subsy*:
           Where to place the subticks between each major tick.
           Should be a sequence of integers.  For example, in a log10
           scale: ``[2, 3, 4, 5, 6, 7, 8, 9]``

           will place 8 logarithmically spaced minor ticks between
           each major tick.

        *linscalex*/*linscaley*:
           This allows the linear range (-*linthresh* to *linthresh*)
           to be stretched relative to the logarithmic range.  Its
           value is the number of decades to use for each half of the
           linear range.  For example, when *linscale* == 1.0 (the
           default), the space used for the positive and negative
           halves of the linear range will be equal to one decade in
           the logarithmic range.
        """
        if axis.axis_name == 'x':
            base = kwargs.pop('basex', 10.0)
            linthresh = kwargs.pop('linthreshx', 2.0)
            subs = kwargs.pop('subsx', None)
            linscale = kwargs.pop('linscalex', 1.0)
        else:
            base = kwargs.pop('basey', 10.0)
            linthresh = kwargs.pop('linthreshy', 2.0)
            subs = kwargs.pop('subsy', None)
            linscale = kwargs.pop('linscaley', 1.0)

        if base <= 1.0:
            raise ValueError("'basex/basey' must be larger than 1")
        if linthresh <= 0.0:
            raise ValueError("'linthreshx/linthreshy' must be positive")
        if linscale <= 0.0:
            raise ValueError("'linscalex/linthreshy' must be positive")

        self._transform = self.SymmetricalLogTransform(base,
                                                       linthresh,
                                                       linscale)

        self.base = base
        self.linthresh = linthresh
        self.linscale = linscale
        self.subs = subs

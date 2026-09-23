    def __init__(self, base=10.0, subs=(1.0,), numdecs=4, numticks=None):
        """
        Place ticks on the locations : subs[j] * base**i

        Parameters
        ----------
        subs : None or str or sequence of float, default: (1.0,)
            Gives the multiples of integer powers of the base at which
            to place ticks.  The default places ticks only at
            integer powers of the base.
            The permitted string values are ``'auto'`` and ``'all'``,
            both of which use an algorithm based on the axis view
            limits to determine whether and how to put ticks between
            integer powers of the base.  With ``'auto'``, ticks are
            placed only between integer powers; with ``'all'``, the
            integer powers are included.  A value of None is
            equivalent to ``'auto'``.

        """
        if numticks is None:
            if mpl.rcParams['_internal.classic_mode']:
                numticks = 15
            else:
                numticks = 'auto'
        self.base(base)
        self.subs(subs)
        self.numdecs = numdecs
        self.numticks = numticks

    @docstring.dedent_interpd
    def loglog(self, *args, **kwargs):
        """
        Make a plot with log scaling on both the *x* and *y* axis.

        :func:`~matplotlib.pyplot.loglog` supports all the keyword
        arguments of :func:`~matplotlib.pyplot.plot` and
        :meth:`matplotlib.axes.Axes.set_xscale` /
        :meth:`matplotlib.axes.Axes.set_yscale`.

        Notable keyword arguments:

          *basex*/*basey*: scalar > 1
            Base of the *x*/*y* logarithm

          *subsx*/*subsy*: [ *None* | sequence ]
            The location of the minor *x*/*y* ticks; *None* defaults
            to autosubs, which depend on the number of decades in the
            plot; see :meth:`matplotlib.axes.Axes.set_xscale` /
            :meth:`matplotlib.axes.Axes.set_yscale` for details

          *nonposx*/*nonposy*: ['mask' | 'clip' ]
            Non-positive values in *x* or *y* can be masked as
            invalid, or clipped to a very small positive number

        The remaining valid kwargs are
        :class:`~matplotlib.lines.Line2D` properties:

        %(Line2D)s

        """
        if not self._hold:
            self.cla()

        dx = {'basex': kwargs.pop('basex', 10),
              'subsx': kwargs.pop('subsx', None),
              'nonposx': kwargs.pop('nonposx', 'mask'),
              }
        dy = {'basey': kwargs.pop('basey', 10),
              'subsy': kwargs.pop('subsy', None),
              'nonposy': kwargs.pop('nonposy', 'mask'),
              }

        self.set_xscale('log', **dx)
        self.set_yscale('log', **dy)

        b = self._hold
        self._hold = True  # we've already processed the hold
        l = self.plot(*args, **kwargs)
        self._hold = b  # restore the hold

        return l

    def axis(self, *args, **kwargs):
        """
        Convenience method to get or set some axis properties.

        Call signatures::

          xmin, xmax, ymin, ymax = axis()
          xmin, xmax, ymin, ymax = axis([xmin, xmax, ymin, ymax])
          xmin, xmax, ymin, ymax = axis(option)
          xmin, xmax, ymin, ymax = axis(**kwargs)

        Parameters
        ----------
        xmin, xmax, ymin, ymax : float, optional
            The axis limits to be set. Either none or all of the limits must
            be given. This can also be achieved using ::

                ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))

        option : bool or str
            If a bool, turns axis lines and labels on or off. If a string,
            possible values are:

            ======== ==========================================================
            Value    Description
            ======== ==========================================================
            'on'     Turn on axis lines and labels. Same as ``True``.
            'off'    Turn off axis lines and labels. Same as ``False``.
            'equal'  Set equal scaling (i.e., make circles circular) by
                     changing axis limits.
            'scaled' Set equal scaling (i.e., make circles circular) by
                     changing dimensions of the plot box.
            'tight'  Set limits just large enough to show all data.
            'auto'   Automatic scaling (fill plot box with data).
            'normal' Same as 'auto'; deprecated.
            'image'  'scaled' with axis limits equal to data limits.
            'square' Square plot; similar to 'scaled', but initially forcing
                     ``xmax-xmin = ymax-ymin``.
            ======== ==========================================================

        emit : bool, optional, default *True*
            Whether observers are notified of the axis limit change.
            This option is passed on to `~.Axes.set_xlim` and
            `~.Axes.set_ylim`.

        Returns
        -------
        xmin, xmax, ymin, ymax : float
            The axis limits.

        See also
        --------
        matplotlib.axes.Axes.set_xlim
        matplotlib.axes.Axes.set_ylim
        """

        if len(args) == len(kwargs) == 0:
            xmin, xmax = self.get_xlim()
            ymin, ymax = self.get_ylim()
            return xmin, xmax, ymin, ymax

        emit = kwargs.get('emit', True)

        if len(args) == 1 and isinstance(args[0], str):
            s = args[0].lower()
            if s == 'on':
                self.set_axis_on()
            elif s == 'off':
                self.set_axis_off()
            elif s in ('equal', 'tight', 'scaled', 'normal',
                       'auto', 'image', 'square'):
                if s == 'normal':
                    cbook.warn_deprecated(
                        "3.1", message="Passing 'normal' to axis() is "
                        "deprecated since %(since)s; use 'auto' instead.")
                self.set_autoscale_on(True)
                self.set_aspect('auto')
                self.autoscale_view(tight=False)
                # self.apply_aspect()
                if s == 'equal':
                    self.set_aspect('equal', adjustable='datalim')
                elif s == 'scaled':
                    self.set_aspect('equal', adjustable='box', anchor='C')
                    self.set_autoscale_on(False)  # Req. by Mark Bakker
                elif s == 'tight':
                    self.autoscale_view(tight=True)
                    self.set_autoscale_on(False)
                elif s == 'image':
                    self.autoscale_view(tight=True)
                    self.set_autoscale_on(False)
                    self.set_aspect('equal', adjustable='box', anchor='C')
                elif s == 'square':
                    self.set_aspect('equal', adjustable='box', anchor='C')
                    self.set_autoscale_on(False)
                    xlim = self.get_xlim()
                    ylim = self.get_ylim()
                    edge_size = max(np.diff(xlim), np.diff(ylim))
                    self.set_xlim([xlim[0], xlim[0] + edge_size],
                                  emit=emit, auto=False)
                    self.set_ylim([ylim[0], ylim[0] + edge_size],
                                  emit=emit, auto=False)
            else:
                raise ValueError('Unrecognized string %s to axis; '
                                 'try on or off' % s)
            xmin, xmax = self.get_xlim()
            ymin, ymax = self.get_ylim()
            return xmin, xmax, ymin, ymax

        try:
            args[0]
        except IndexError:
            xmin = kwargs.get('xmin', None)
            xmax = kwargs.get('xmax', None)
            auto = False  # turn off autoscaling, unless...
            if xmin is None and xmax is None:
                auto = None  # leave autoscaling state alone
            xmin, xmax = self.set_xlim(xmin, xmax, emit=emit, auto=auto)

            ymin = kwargs.get('ymin', None)
            ymax = kwargs.get('ymax', None)
            auto = False  # turn off autoscaling, unless...
            if ymin is None and ymax is None:
                auto = None  # leave autoscaling state alone
            ymin, ymax = self.set_ylim(ymin, ymax, emit=emit, auto=auto)
            return xmin, xmax, ymin, ymax

        v = args[0]
        if isinstance(v, bool):
            if v:
                self.set_axis_on()
            else:
                self.set_axis_off()
            xmin, xmax = self.get_xlim()
            ymin, ymax = self.get_ylim()
            return xmin, xmax, ymin, ymax

        if len(v) != 4:
            raise ValueError('args must contain [xmin xmax ymin ymax]')

        self.set_xlim([v[0], v[1]], emit=emit, auto=False)
        self.set_ylim([v[2], v[3]], emit=emit, auto=False)

        return v

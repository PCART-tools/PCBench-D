    def axis(self, *args, emit=True, **kwargs):
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
            The axis limits to be set.  This can also be achieved using ::

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
                     changing axis limits. This is the same as
                     ``ax.set_aspect('equal', adjustable='datalim')``.
                     Explicit data limits may not be respected in this case.
            'scaled' Set equal scaling (i.e., make circles circular) by
                     changing dimensions of the plot box. This is the same as
                     ``ax.set_aspect('equal', adjustable='box', anchor='C')``.
                     Additionally, further autoscaling will be disabled.
            'tight'  Set limits just large enough to show all data, then
                     disable further autoscaling.
            'auto'   Automatic scaling (fill plot box with data).
            'normal' Same as 'auto'; deprecated.
            'image'  'scaled' with axis limits equal to data limits.
            'square' Square plot; similar to 'scaled', but initially forcing
                     ``xmax-xmin == ymax-ymin``.
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
        if len(args) == 1 and isinstance(args[0], (str, bool)):
            s = args[0]
            if s is True:
                s = 'on'
            if s is False:
                s = 'off'
            s = s.lower()
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
                    edge_size = max(np.diff(xlim), np.diff(ylim))[0]
                    self.set_xlim([xlim[0], xlim[0] + edge_size],
                                  emit=emit, auto=False)
                    self.set_ylim([ylim[0], ylim[0] + edge_size],
                                  emit=emit, auto=False)
            else:
                raise ValueError('Unrecognized string %s to axis; '
                                 'try on or off' % s)
        else:
            if len(args) >= 1:
                if len(args) != 1:
                    cbook.warn_deprecated(
                        "3.2", message="Passing more than one positional "
                        "argument to axis() is deprecated and will raise a "
                        "TypeError %(removal)s.")
                limits = args[0]
                try:
                    xmin, xmax, ymin, ymax = limits
                except (TypeError, ValueError):
                    raise TypeError('the first argument to axis() must be an '
                                    'interable of the form '
                                    '[xmin, xmax, ymin, ymax]')
            else:
                xmin = kwargs.pop('xmin', None)
                xmax = kwargs.pop('xmax', None)
                ymin = kwargs.pop('ymin', None)
                ymax = kwargs.pop('ymax', None)
            xauto = (None  # Keep autoscale state as is.
                     if xmin is None and xmax is None
                     else False)  # Turn off autoscale.
            yauto = (None
                     if ymin is None and ymax is None
                     else False)
            self.set_xlim(xmin, xmax, emit=emit, auto=xauto)
            self.set_ylim(ymin, ymax, emit=emit, auto=yauto)
        if kwargs:
            cbook.warn_deprecated(
                "3.1", message="Passing unsupported keyword arguments to "
                "axis() will raise a TypeError %(removal)s.")
        return (*self.get_xlim(), *self.get_ylim())

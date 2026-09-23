    def axis(self, arg=None, /, *, emit=True, **kwargs):
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

            ================ ===========================================================
            Value            Description
            ================ ===========================================================
            'off' or `False` Hide all axis decorations, i.e. axis labels, spines,
                             tick marks, tick labels, and grid lines.
                             This is the same as `~.Axes.set_axis_off()`.
            'on' or `True`   Do not hide all axis decorations, i.e. axis labels, spines,
                             tick marks, tick labels, and grid lines.
                             This is the same as `~.Axes.set_axis_on()`.
            'equal'          Set equal scaling (i.e., make circles circular) by
                             changing the axis limits. This is the same as
                             ``ax.set_aspect('equal', adjustable='datalim')``.
                             Explicit data limits may not be respected in this case.
            'scaled'         Set equal scaling (i.e., make circles circular) by
                             changing dimensions of the plot box. This is the same as
                             ``ax.set_aspect('equal', adjustable='box', anchor='C')``.
                             Additionally, further autoscaling will be disabled.
            'tight'          Set limits just large enough to show all data, then
                             disable further autoscaling.
            'auto'           Automatic scaling (fill plot box with data).
            'image'          'scaled' with axis limits equal to data limits.
            'square'         Square plot; similar to 'scaled', but initially forcing
                             ``xmax-xmin == ymax-ymin``.
            ================ ===========================================================

        emit : bool, default: True
            Whether observers are notified of the axis limit change.
            This option is passed on to `~.Axes.set_xlim` and
            `~.Axes.set_ylim`.

        Returns
        -------
        xmin, xmax, ymin, ymax : float
            The axis limits.

        See Also
        --------
        matplotlib.axes.Axes.set_xlim
        matplotlib.axes.Axes.set_ylim

        Notes
        -----
        For 3D Axes, this method additionally takes *zmin*, *zmax* as
        parameters and likewise returns them.
        """
        if isinstance(arg, (str, bool)):
            if arg is True:
                arg = 'on'
            if arg is False:
                arg = 'off'
            arg = arg.lower()
            if arg == 'on':
                self.set_axis_on()
            elif arg == 'off':
                self.set_axis_off()
            elif arg in [
                    'equal', 'tight', 'scaled', 'auto', 'image', 'square']:
                self.set_autoscale_on(True)
                self.set_aspect('auto')
                self.autoscale_view(tight=False)
                if arg == 'equal':
                    self.set_aspect('equal', adjustable='datalim')
                elif arg == 'scaled':
                    self.set_aspect('equal', adjustable='box', anchor='C')
                    self.set_autoscale_on(False)  # Req. by Mark Bakker
                elif arg == 'tight':
                    self.autoscale_view(tight=True)
                    self.set_autoscale_on(False)
                elif arg == 'image':
                    self.autoscale_view(tight=True)
                    self.set_autoscale_on(False)
                    self.set_aspect('equal', adjustable='box', anchor='C')
                elif arg == 'square':
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
                raise ValueError(f"Unrecognized string {arg!r} to axis; "
                                 "try 'on' or 'off'")
        else:
            if arg is not None:
                if len(arg) != 2*len(self._axis_names):
                    raise TypeError(
                        "The first argument to axis() must be an iterable of the form "
                        "[{}]".format(", ".join(
                            f"{name}min, {name}max" for name in self._axis_names)))
                limits = {
                    name: arg[2*i:2*(i+1)]
                    for i, name in enumerate(self._axis_names)
                }
            else:
                limits = {}
                for name in self._axis_names:
                    ax_min = kwargs.pop(f'{name}min', None)
                    ax_max = kwargs.pop(f'{name}max', None)
                    limits[name] = (ax_min, ax_max)
            for name, (ax_min, ax_max) in limits.items():
                ax_auto = (None  # Keep autoscale state as is.
                           if ax_min is None and ax_max is None
                           else False)  # Turn off autoscale.
                set_ax_lim = getattr(self, f'set_{name}lim')
                set_ax_lim(ax_min, ax_max, emit=emit, auto=ax_auto)
        if kwargs:
            raise _api.kwarg_error("axis", kwargs)
        lims = ()
        for name in self._axis_names:
            get_ax_lim = getattr(self, f'get_{name}lim')
            lims += get_ax_lim()
        return lims

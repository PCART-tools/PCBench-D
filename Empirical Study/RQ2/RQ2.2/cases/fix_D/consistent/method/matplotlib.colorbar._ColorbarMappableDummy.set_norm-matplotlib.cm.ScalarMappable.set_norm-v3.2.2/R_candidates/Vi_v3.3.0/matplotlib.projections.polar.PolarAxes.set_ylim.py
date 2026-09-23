    def set_ylim(self, bottom=None, top=None, emit=True, auto=False,
                 *, ymin=None, ymax=None):
        """
        Set the data limits for the radial axis.

        Parameters
        ----------
        bottom : float, optional
            The bottom limit (default: None, which leaves the bottom
            limit unchanged).
            The bottom and top ylims may be passed as the tuple
            (*bottom*, *top*) as the first positional argument (or as
            the *bottom* keyword argument).

        top : float, optional
            The top limit (default: None, which leaves the top limit
            unchanged).

        emit : bool, default: True
            Whether to notify observers of limit change.

        auto : bool or None, default: False
            Whether to turn on autoscaling of the y-axis. True turns on,
            False turns off, None leaves unchanged.

        ymin, ymax : float, optional
            These arguments are deprecated and will be removed in a future
            version.  They are equivalent to *bottom* and *top* respectively,
            and it is an error to pass both *ymin* and *bottom* or
            *ymax* and *top*.

        Returns
        -------
        bottom, top : (float, float)
            The new y-axis limits in data coordinates.
        """
        if ymin is not None:
            if bottom is not None:
                raise ValueError('Cannot supply both positional "bottom" '
                                 'argument and kwarg "ymin"')
            else:
                bottom = ymin
        if ymax is not None:
            if top is not None:
                raise ValueError('Cannot supply both positional "top" '
                                 'argument and kwarg "ymax"')
            else:
                top = ymax
        if top is None and np.iterable(bottom):
            bottom, top = bottom[0], bottom[1]
        return super().set_ylim(bottom=bottom, top=top, emit=emit, auto=auto)

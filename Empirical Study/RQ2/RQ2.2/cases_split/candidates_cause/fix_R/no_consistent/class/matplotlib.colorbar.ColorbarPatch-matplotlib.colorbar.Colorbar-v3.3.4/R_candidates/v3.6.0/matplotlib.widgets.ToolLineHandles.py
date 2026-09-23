class ToolLineHandles:
    """
    Control handles for canvas tools.

    Parameters
    ----------
    ax : `matplotlib.axes.Axes`
        Matplotlib Axes where tool handles are displayed.
    positions : 1D array
        Positions of handles in data coordinates.
    direction : {"horizontal", "vertical"}
        Direction of handles, either 'vertical' or 'horizontal'
    line_props : dict, optional
        Additional line properties. See `matplotlib.lines.Line2D`.
    useblit : bool, default: True
        Whether to use blitting for faster drawing (if supported by the
        backend). See the tutorial :doc:`/tutorials/advanced/blitting`
        for details.
    """

    def __init__(self, ax, positions, direction, line_props=None,
                 useblit=True):
        self.ax = ax

        _api.check_in_list(['horizontal', 'vertical'], direction=direction)
        self._direction = direction

        if line_props is None:
            line_props = {}
        line_props.update({'visible': False, 'animated': useblit})

        line_fun = ax.axvline if self.direction == 'horizontal' else ax.axhline

        self._artists = [line_fun(p, **line_props) for p in positions]

    @property
    def artists(self):
        return tuple(self._artists)

    @property
    def positions(self):
        """Positions of the handle in data coordinates."""
        method = 'get_xdata' if self.direction == 'horizontal' else 'get_ydata'
        return [getattr(line, method)()[0] for line in self.artists]

    @property
    def direction(self):
        """Direction of the handle: 'vertical' or 'horizontal'."""
        return self._direction

    def set_data(self, positions):
        """
        Set x or y positions of handles, depending if the lines are vertical
        of horizontal.

        Parameters
        ----------
        positions : tuple of length 2
            Set the positions of the handle in data coordinates
        """
        method = 'set_xdata' if self.direction == 'horizontal' else 'set_ydata'
        for line, p in zip(self.artists, positions):
            getattr(line, method)([p, p])

    def set_visible(self, value):
        """Set the visibility state of the handles artist."""
        for artist in self.artists:
            artist.set_visible(value)

    def set_animated(self, value):
        """Set the animated state of the handles artist."""
        for artist in self.artists:
            artist.set_animated(value)

    def remove(self):
        """Remove the handles artist from the figure."""
        for artist in self._artists:
            artist.remove()

    def closest(self, x, y):
        """
        Return index and pixel distance to closest handle.

        Parameters
        ----------
        x, y : float
            x, y position from which the distance will be calculated to
            determinate the closest handle

        Returns
        -------
        index, distance : index of the handle and its distance from
            position x, y
        """
        if self.direction == 'horizontal':
            p_pts = np.array([
                self.ax.transData.transform((p, 0))[0] for p in self.positions
                ])
            dist = abs(p_pts - x)
        else:
            p_pts = np.array([
                self.ax.transData.transform((0, p))[1] for p in self.positions
                ])
            dist = abs(p_pts - y)
        index = np.argmin(dist)
        return index, dist[index]

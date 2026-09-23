class SpanSelector(_SelectorWidget):
    """
    Visually select a min/max range on a single axis and call a function with
    those values.

    To guarantee that the selector remains responsive, keep a reference to it.

    In order to turn off the SpanSelector, set ``span_selector.active`` to
    False.  To turn it back on, set it to True.

    Parameters
    ----------
    ax : `matplotlib.axes.Axes`

    onselect : func(min, max), min/max are floats

    direction : {"horizontal", "vertical"}
        The direction along which to draw the span selector.

    minspan : float, default: None
        If selection is less than *minspan*, do not call *onselect*.

    useblit : bool, default: False
        If True, use the backend-dependent blitting features for faster
        canvas updates.

    rectprops : dict, default: None
        Dictionary of `matplotlib.patches.Patch` properties.

    onmove_callback : func(min, max), min/max are floats, default: None
        Called on mouse move while the span is being selected.

    span_stays : bool, default: False
        If True, the span stays visible after the mouse is released.

    button : `.MouseButton` or list of `.MouseButton`
        The mouse buttons which activate the span selector.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import matplotlib.widgets as mwidgets
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [10, 50, 100])
    >>> def onselect(vmin, vmax):
    ...     print(vmin, vmax)
    >>> rectprops = dict(facecolor='blue', alpha=0.5)
    >>> span = mwidgets.SpanSelector(ax, onselect, 'horizontal',
    ...                              rectprops=rectprops)
    >>> fig.show()

    See also: :doc:`/gallery/widgets/span_selector`
    """

    def __init__(self, ax, onselect, direction, minspan=None, useblit=False,
                 rectprops=None, onmove_callback=None, span_stays=False,
                 button=None):

        super().__init__(ax, onselect, useblit=useblit, button=button)

        if rectprops is None:
            rectprops = dict(facecolor='red', alpha=0.5)

        rectprops['animated'] = self.useblit

        _api.check_in_list(['horizontal', 'vertical'], direction=direction)
        self.direction = direction

        self.rect = None
        self.pressv = None

        self.rectprops = rectprops
        self.onmove_callback = onmove_callback
        self.minspan = minspan
        self.span_stays = span_stays

        # Needed when dragging out of axes
        self.prev = (0, 0)

        # Reset canvas so that `new_axes` connects events.
        self.canvas = None
        self.new_axes(ax)

    def new_axes(self, ax):
        """Set SpanSelector to operate on a new Axes."""
        self.ax = ax
        if self.canvas is not ax.figure.canvas:
            if self.canvas is not None:
                self.disconnect_events()

            self.canvas = ax.figure.canvas
            self.connect_default_events()

        if self.direction == 'horizontal':
            trans = ax.get_xaxis_transform()
            w, h = 0, 1
        else:
            trans = ax.get_yaxis_transform()
            w, h = 1, 0
        self.rect = Rectangle((0, 0), w, h,
                              transform=trans,
                              visible=False,
                              **self.rectprops)
        if self.span_stays:
            self.stay_rect = Rectangle((0, 0), w, h,
                                       transform=trans,
                                       visible=False,
                                       **self.rectprops)
            self.stay_rect.set_animated(False)
            self.ax.add_patch(self.stay_rect)

        self.ax.add_patch(self.rect)
        self.artists = [self.rect]

    def ignore(self, event):
        # docstring inherited
        return super().ignore(event) or not self.visible

    def _press(self, event):
        """Button press event handler."""
        self.rect.set_visible(self.visible)
        if self.span_stays:
            self.stay_rect.set_visible(False)
            # really force a draw so that the stay rect is not in
            # the blit background
            if self.useblit:
                self.canvas.draw()
        xdata, ydata = self._get_data(event)
        if self.direction == 'horizontal':
            self.pressv = xdata
        else:
            self.pressv = ydata

        self._set_span_xy(event)
        return False

    def _release(self, event):
        """Button release event handler."""
        if self.pressv is None:
            return

        self.rect.set_visible(False)

        if self.span_stays:
            self.stay_rect.set_x(self.rect.get_x())
            self.stay_rect.set_y(self.rect.get_y())
            self.stay_rect.set_width(self.rect.get_width())
            self.stay_rect.set_height(self.rect.get_height())
            self.stay_rect.set_visible(True)

        self.canvas.draw_idle()
        vmin = self.pressv
        xdata, ydata = self._get_data(event)
        if self.direction == 'horizontal':
            vmax = xdata or self.prev[0]
        else:
            vmax = ydata or self.prev[1]

        if vmin > vmax:
            vmin, vmax = vmax, vmin
        span = vmax - vmin
        if self.minspan is not None and span < self.minspan:
            return
        self.onselect(vmin, vmax)
        self.pressv = None
        return False

    def _onmove(self, event):
        """Motion notify event handler."""
        if self.pressv is None:
            return

        self._set_span_xy(event)

        if self.onmove_callback is not None:
            vmin = self.pressv
            xdata, ydata = self._get_data(event)
            if self.direction == 'horizontal':
                vmax = xdata or self.prev[0]
            else:
                vmax = ydata or self.prev[1]

            if vmin > vmax:
                vmin, vmax = vmax, vmin
            self.onmove_callback(vmin, vmax)

        self.update()
        return False

    def _set_span_xy(self, event):
        """Set the span coordinates."""
        x, y = self._get_data(event)
        if x is None:
            return

        self.prev = x, y
        if self.direction == 'horizontal':
            v = x
        else:
            v = y

        minv, maxv = v, self.pressv
        if minv > maxv:
            minv, maxv = maxv, minv
        if self.direction == 'horizontal':
            self.rect.set_x(minv)
            self.rect.set_width(maxv - minv)
        else:
            self.rect.set_y(minv)
            self.rect.set_height(maxv - minv)

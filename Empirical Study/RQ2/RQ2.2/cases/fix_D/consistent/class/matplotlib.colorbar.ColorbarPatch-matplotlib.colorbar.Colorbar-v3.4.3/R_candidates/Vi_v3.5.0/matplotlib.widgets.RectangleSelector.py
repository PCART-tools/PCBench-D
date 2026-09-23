@docstring.Substitution(_RECTANGLESELECTOR_PARAMETERS_DOCSTRING.replace(
    '__ARTIST_NAME__', 'rectangle'))
class RectangleSelector(_SelectorWidget):
    """
    Select a rectangular region of an axes.

    For the cursor to remain responsive you must keep a reference to it.

    Press and release events triggered at the same coordinates outside the
    selection will clear the selector, except when
    ``ignore_event_outside=True``.

    %s

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import matplotlib.widgets as mwidgets
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [10, 50, 100])
    >>> def onselect(eclick, erelease):
    ...     print(eclick.xdata, eclick.ydata)
    ...     print(erelease.xdata, erelease.ydata)
    >>> props = dict(facecolor='blue', alpha=0.5)
    >>> rect = mwidgets.RectangleSelector(ax, onselect, interactive=True,
                                          props=props)
    >>> fig.show()

    See also: :doc:`/gallery/widgets/rectangle_selector`
    """

    _shape_klass = Rectangle

    @_api.rename_parameter("3.5", "maxdist", "grab_range")
    @_api.rename_parameter("3.5", "marker_props", "handle_props")
    @_api.rename_parameter("3.5", "rectprops", "props")
    @_api.delete_parameter("3.5", "drawtype")
    @_api.delete_parameter("3.5", "lineprops")
    def __init__(self, ax, onselect, drawtype='box',
                 minspanx=0, minspany=0, useblit=False,
                 lineprops=None, props=None, spancoords='data',
                 button=None, grab_range=10, handle_props=None,
                 interactive=False, state_modifier_keys=None,
                 drag_from_anywhere=False, ignore_event_outside=False):
        super().__init__(ax, onselect, useblit=useblit, button=button,
                         state_modifier_keys=state_modifier_keys)

        self.visible = True
        self._interactive = interactive
        self.drag_from_anywhere = drag_from_anywhere
        self.ignore_event_outside = ignore_event_outside

        if drawtype == 'none':  # draw a line but make it invisible
            _api.warn_deprecated(
                "3.5", message="Support for drawtype='none' is deprecated "
                               "since %(since)s and will be removed "
                               "%(removal)s."
                               "Use props=dict(visible=False) instead.")
            drawtype = 'line'
            self.visible = False

        if drawtype == 'box':
            if props is None:
                props = dict(facecolor='red', edgecolor='black',
                             alpha=0.2, fill=True)
            props['animated'] = self.useblit
            self.visible = props.pop('visible', self.visible)
            self._props = props
            to_draw = self._shape_klass((0, 0), 0, 1, visible=False,
                                        **self._props)
            self.ax.add_patch(to_draw)
        if drawtype == 'line':
            _api.warn_deprecated(
                "3.5", message="Support for drawtype='line' is deprecated "
                               "since %(since)s and will be removed "
                               "%(removal)s.")
            if lineprops is None:
                lineprops = dict(color='black', linestyle='-',
                                 linewidth=2, alpha=0.5)
            lineprops['animated'] = self.useblit
            self._props = lineprops
            to_draw = Line2D([0, 0], [0, 0], visible=False, **self._props)
            self.ax.add_line(to_draw)

        self._selection_artist = to_draw

        self.minspanx = minspanx
        self.minspany = minspany

        _api.check_in_list(['data', 'pixels'], spancoords=spancoords)
        self.spancoords = spancoords
        self._drawtype = drawtype

        self.grab_range = grab_range

        if self._interactive:
            self._handle_props = {
                'markeredgecolor': (self._props or {}).get(
                    'edgecolor', 'black'),
                **cbook.normalize_kwargs(handle_props, Line2D)}

            self._corner_order = ['SW', 'SE', 'NE', 'NW']
            xc, yc = self.corners
            self._corner_handles = ToolHandles(self.ax, xc, yc,
                                               marker_props=self._handle_props,
                                               useblit=self.useblit)

            self._edge_order = ['W', 'S', 'E', 'N']
            xe, ye = self.edge_centers
            self._edge_handles = ToolHandles(self.ax, xe, ye, marker='s',
                                             marker_props=self._handle_props,
                                             useblit=self.useblit)

            xc, yc = self.center
            self._center_handle = ToolHandles(self.ax, [xc], [yc], marker='s',
                                              marker_props=self._handle_props,
                                              useblit=self.useblit)

            self._active_handle = None

        self._extents_on_press = None

    to_draw = _api.deprecated("3.5")(
        property(lambda self: self._selection_artist)
        )

    drawtype = _api.deprecate_privatize_attribute("3.5")

    active_handle = _api.deprecate_privatize_attribute("3.5")

    interactive = _api.deprecate_privatize_attribute("3.5")

    maxdist = _api.deprecated("3.5", name="maxdist", alternative="grab_range")(
        property(lambda self: self.grab_range,
                 lambda self, value: setattr(self, "grab_range", value)))

    @property
    def _handles_artists(self):
        return (*self._center_handle.artists, *self._corner_handles.artists,
                *self._edge_handles.artists)

    def _press(self, event):
        """Button press event handler."""
        # make the drawn box/line visible get the click-coordinates,
        # button, ...
        if self._interactive and self._selection_artist.get_visible():
            self._set_active_handle(event)
            self._extents_on_press = self.extents
        else:
            self._active_handle = None

        if self._active_handle is None or not self._interactive:
            # Clear previous rectangle before drawing new rectangle.
            self.update()

        if self._active_handle is None and not self.ignore_event_outside:
            x = event.xdata
            y = event.ydata
            self.visible = False
            self.extents = x, x, y, y
            self.visible = True
        else:
            self.set_visible(True)

        return False

    def _release(self, event):
        """Button release event handler."""
        if not self._interactive:
            self._selection_artist.set_visible(False)

        if (self._active_handle is None and self._selection_completed and
                self.ignore_event_outside):
            return

        # update the eventpress and eventrelease with the resulting extents
        x0, x1, y0, y1 = self.extents
        self._eventpress.xdata = x0
        self._eventpress.ydata = y0
        xy0 = self.ax.transData.transform([x0, y0])
        self._eventpress.x, self._eventpress.y = xy0

        self._eventrelease.xdata = x1
        self._eventrelease.ydata = y1
        xy1 = self.ax.transData.transform([x1, y1])
        self._eventrelease.x, self._eventrelease.y = xy1

        # calculate dimensions of box or line
        if self.spancoords == 'data':
            spanx = abs(self._eventpress.xdata - self._eventrelease.xdata)
            spany = abs(self._eventpress.ydata - self._eventrelease.ydata)
        elif self.spancoords == 'pixels':
            spanx = abs(self._eventpress.x - self._eventrelease.x)
            spany = abs(self._eventpress.y - self._eventrelease.y)
        else:
            _api.check_in_list(['data', 'pixels'],
                               spancoords=self.spancoords)
        # check if drawn distance (if it exists) is not too small in
        # either x or y-direction
        minspanxy = (spanx <= self.minspanx or spany <= self.minspany)
        if (self._drawtype != 'none' and minspanxy):
            for artist in self.artists:
                artist.set_visible(False)
            if self._selection_completed:
                # Call onselect, only when the selection is already existing
                self.onselect(self._eventpress, self._eventrelease)
            self._selection_completed = False
        else:
            self.onselect(self._eventpress, self._eventrelease)
            self._selection_completed = True

        self.update()
        self._active_handle = None
        self._extents_on_press = None

        return False

    def _onmove(self, event):
        """Motion notify event handler."""

        state = self._state | self._default_state
        # resize an existing shape
        if self._active_handle and self._active_handle != 'C':
            x0, x1, y0, y1 = self._extents_on_press
            size_on_press = [x1 - x0, y1 - y0]
            center = [x0 + size_on_press[0] / 2, y0 + size_on_press[1] / 2]
            dx = event.xdata - self._eventpress.xdata
            dy = event.ydata - self._eventpress.ydata

            # change sign of relative changes to simplify calculation
            # Switch variables so that only x1 and/or y1 are updated on move
            x_factor = y_factor = 1
            if 'W' in self._active_handle:
                x_factor *= -1
                dx *= x_factor
                x0 = x1
            if 'S' in self._active_handle:
                y_factor *= -1
                dy *= y_factor
                y0 = y1

            # Keeping the center fixed
            if 'center' in state:
                if 'square' in state:
                    # Force the same change in dx and dy
                    if self._active_handle in ['E', 'W']:
                        # using E, W handle we need to update dy accordingly
                        dy = dx
                    elif self._active_handle in ['S', 'N']:
                        # using S, N handle, we need to update dx accordingly
                        dx = dy
                    else:
                        dx = dy = max(dx, dy, key=abs)

                # new half-width and half-height
                hw = size_on_press[0] / 2 + dx
                hh = size_on_press[1] / 2 + dy

                if 'square' not in state:
                    # cancel changes in perpendicular direction
                    if self._active_handle in ['E', 'W']:
                        hh = size_on_press[1] / 2
                    if self._active_handle in ['N', 'S']:
                        hw = size_on_press[0] / 2

                x0, x1, y0, y1 = (center[0] - hw, center[0] + hw,
                                  center[1] - hh, center[1] + hh)

            else:
                # Keeping the opposite corner/edge fixed
                if 'square' in state:
                    dx = dy = max(dx, dy, key=abs)
                    x1 = x0 + x_factor * (dx + size_on_press[0])
                    y1 = y0 + y_factor * (dy + size_on_press[1])
                else:
                    if self._active_handle in ['E', 'W'] + self._corner_order:
                        x1 = event.xdata
                    if self._active_handle in ['N', 'S'] + self._corner_order:
                        y1 = event.ydata

        # move existing shape
        elif (self._active_handle == 'C' or
              (self.drag_from_anywhere and self._contains(event)) and
              self._extents_on_press is not None):
            x0, x1, y0, y1 = self._extents_on_press
            dx = event.xdata - self._eventpress.xdata
            dy = event.ydata - self._eventpress.ydata
            x0 += dx
            x1 += dx
            y0 += dy
            y1 += dy

        # new shape
        else:
            # Don't create a new rectangle if there is already one when
            # ignore_event_outside=True
            if self.ignore_event_outside and self._selection_completed:
                return
            center = [self._eventpress.xdata, self._eventpress.ydata]
            center_pix = [self._eventpress.x, self._eventpress.y]
            dx = (event.xdata - center[0]) / 2.
            dy = (event.ydata - center[1]) / 2.

            # square shape
            if 'square' in state:
                dx_pix = abs(event.x - center_pix[0])
                dy_pix = abs(event.y - center_pix[1])
                if not dx_pix:
                    return
                maxd = max(abs(dx_pix), abs(dy_pix))
                if abs(dx_pix) < maxd:
                    dx *= maxd / (abs(dx_pix) + 1e-6)
                if abs(dy_pix) < maxd:
                    dy *= maxd / (abs(dy_pix) + 1e-6)

            # from center
            if 'center' in state:
                dx *= 2
                dy *= 2

            # from corner
            else:
                center[0] += dx
                center[1] += dy

            x0, x1, y0, y1 = (center[0] - dx, center[0] + dx,
                              center[1] - dy, center[1] + dy)

        self.extents = x0, x1, y0, y1

    @property
    def _rect_bbox(self):
        if self._drawtype == 'box':
            x0 = self._selection_artist.get_x()
            y0 = self._selection_artist.get_y()
            width = self._selection_artist.get_width()
            height = self._selection_artist.get_height()
            return x0, y0, width, height
        else:
            x, y = self._selection_artist.get_data()
            x0, x1 = min(x), max(x)
            y0, y1 = min(y), max(y)
            return x0, y0, x1 - x0, y1 - y0

    @property
    def corners(self):
        """Corners of rectangle from lower left, moving clockwise."""
        x0, y0, width, height = self._rect_bbox
        xc = x0, x0 + width, x0 + width, x0
        yc = y0, y0, y0 + height, y0 + height
        return xc, yc

    @property
    def edge_centers(self):
        """Midpoint of rectangle edges from left, moving anti-clockwise."""
        x0, y0, width, height = self._rect_bbox
        w = width / 2.
        h = height / 2.
        xe = x0, x0 + w, x0 + width, x0 + w
        ye = y0 + h, y0, y0 + h, y0 + height
        return xe, ye

    @property
    def center(self):
        """Center of rectangle."""
        x0, y0, width, height = self._rect_bbox
        return x0 + width / 2., y0 + height / 2.

    @property
    def extents(self):
        """Return (xmin, xmax, ymin, ymax)."""
        x0, y0, width, height = self._rect_bbox
        xmin, xmax = sorted([x0, x0 + width])
        ymin, ymax = sorted([y0, y0 + height])
        return xmin, xmax, ymin, ymax

    @extents.setter
    def extents(self, extents):
        # Update displayed shape
        self._draw_shape(extents)
        if self._interactive:
            # Update displayed handles
            self._corner_handles.set_data(*self.corners)
            self._edge_handles.set_data(*self.edge_centers)
            self._center_handle.set_data(*self.center)
        self.set_visible(self.visible)
        self.update()

    draw_shape = _api.deprecate_privatize_attribute('3.5')

    def _draw_shape(self, extents):
        x0, x1, y0, y1 = extents
        xmin, xmax = sorted([x0, x1])
        ymin, ymax = sorted([y0, y1])
        xlim = sorted(self.ax.get_xlim())
        ylim = sorted(self.ax.get_ylim())

        xmin = max(xlim[0], xmin)
        ymin = max(ylim[0], ymin)
        xmax = min(xmax, xlim[1])
        ymax = min(ymax, ylim[1])

        if self._drawtype == 'box':
            self._selection_artist.set_x(xmin)
            self._selection_artist.set_y(ymin)
            self._selection_artist.set_width(xmax - xmin)
            self._selection_artist.set_height(ymax - ymin)

        elif self._drawtype == 'line':
            self._selection_artist.set_data([xmin, xmax], [ymin, ymax])

    def _set_active_handle(self, event):
        """Set active handle based on the location of the mouse event."""
        # Note: event.xdata/ydata in data coordinates, event.x/y in pixels
        c_idx, c_dist = self._corner_handles.closest(event.x, event.y)
        e_idx, e_dist = self._edge_handles.closest(event.x, event.y)
        m_idx, m_dist = self._center_handle.closest(event.x, event.y)

        if 'move' in self._state:
            self._active_handle = 'C'
        # Set active handle as closest handle, if mouse click is close enough.
        elif m_dist < self.grab_range * 2:
            # Prioritise center handle over other handles
            self._active_handle = 'C'
        elif (c_dist > self.grab_range and
                  e_dist > self.grab_range):
            # Not close to any handles
            if self.drag_from_anywhere and self._contains(event):
                # Check if we've clicked inside the region
                self._active_handle = 'C'
            else:
                self._active_handle = None
                return
        elif c_dist < e_dist:
            # Closest to a corner handle
            self._active_handle = self._corner_order[c_idx]
        else:
            # Closest to an edge handle
            self._active_handle = self._edge_order[e_idx]

    def _contains(self, event):
        """Return True if event is within the patch."""
        return self._selection_artist.contains(event, radius=0)[0]

    @property
    def geometry(self):
        """
        Return an array of shape (2, 5) containing the
        x (``RectangleSelector.geometry[1, :]``) and
        y (``RectangleSelector.geometry[0, :]``) coordinates
        of the four corners of the rectangle starting and ending
        in the top left corner.
        """
        if hasattr(self._selection_artist, 'get_verts'):
            xfm = self.ax.transData.inverted()
            y, x = xfm.transform(self._selection_artist.get_verts()).T
            return np.array([x, y])
        else:
            return np.array(self._selection_artist.get_data())

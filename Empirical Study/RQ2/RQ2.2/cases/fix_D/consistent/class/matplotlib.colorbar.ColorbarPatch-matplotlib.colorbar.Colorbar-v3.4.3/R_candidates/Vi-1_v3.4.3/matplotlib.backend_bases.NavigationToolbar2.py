class NavigationToolbar2:
    """
    Base class for the navigation cursor, version 2.

    Backends must implement a canvas that handles connections for
    'button_press_event' and 'button_release_event'.  See
    :meth:`FigureCanvasBase.mpl_connect` for more information.

    They must also define

      :meth:`save_figure`
         save the current figure

      :meth:`set_cursor`
         if you want the pointer icon to change

      :meth:`draw_rubberband` (optional)
         draw the zoom to rect "rubberband" rectangle

      :meth:`set_message` (optional)
         display message

      :meth:`set_history_buttons` (optional)
         you can change the history back / forward buttons to
         indicate disabled / enabled state.

    and override ``__init__`` to set up the toolbar -- without forgetting to
    call the base-class init.  Typically, ``__init__`` needs to set up toolbar
    buttons connected to the `home`, `back`, `forward`, `pan`, `zoom`, and
    `save_figure` methods and using standard icons in the "images" subdirectory
    of the data path.

    That's it, we'll do the rest!
    """

    # list of toolitems to add to the toolbar, format is:
    # (
    #   text, # the text of the button (often not visible to users)
    #   tooltip_text, # the tooltip shown on hover (where possible)
    #   image_file, # name of the image for the button (without the extension)
    #   name_of_method, # name of the method in NavigationToolbar2 to call
    # )
    toolitems = (
        ('Home', 'Reset original view', 'home', 'home'),
        ('Back', 'Back to previous view', 'back', 'back'),
        ('Forward', 'Forward to next view', 'forward', 'forward'),
        (None, None, None, None),
        ('Pan',
         'Left button pans, Right button zooms\n'
         'x/y fixes axis, CTRL fixes aspect',
         'move', 'pan'),
        ('Zoom', 'Zoom to rectangle\nx/y fixes axis, CTRL fixes aspect',
         'zoom_to_rect', 'zoom'),
        ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
        (None, None, None, None),
        ('Save', 'Save the figure', 'filesave', 'save_figure'),
      )

    def __init__(self, canvas):
        self.canvas = canvas
        canvas.toolbar = self
        self._nav_stack = cbook.Stack()
        # This cursor will be set after the initial draw.
        self._lastCursor = cursors.POINTER

        init = _api.deprecate_method_override(
            __class__._init_toolbar, self, allow_empty=True, since="3.3",
            addendum="Please fully initialize the toolbar in your subclass' "
            "__init__; a fully empty _init_toolbar implementation may be kept "
            "for compatibility with earlier versions of Matplotlib.")
        if init:
            init()

        self._id_press = self.canvas.mpl_connect(
            'button_press_event', self._zoom_pan_handler)
        self._id_release = self.canvas.mpl_connect(
            'button_release_event', self._zoom_pan_handler)
        self._id_drag = self.canvas.mpl_connect(
            'motion_notify_event', self.mouse_move)
        self._pan_info = None
        self._zoom_info = None

        self.mode = _Mode.NONE  # a mode string for the status bar
        self.set_history_buttons()

    def set_message(self, s):
        """Display a message on toolbar or in status bar."""

    def draw_rubberband(self, event, x0, y0, x1, y1):
        """
        Draw a rectangle rubberband to indicate zoom limits.

        Note that it is not guaranteed that ``x0 <= x1`` and ``y0 <= y1``.
        """

    def remove_rubberband(self):
        """Remove the rubberband."""

    def home(self, *args):
        """
        Restore the original view.

        For convenience of being directly connected as a GUI callback, which
        often get passed additional parameters, this method accepts arbitrary
        parameters, but does not use them.
        """
        self._nav_stack.home()
        self.set_history_buttons()
        self._update_view()

    def back(self, *args):
        """
        Move back up the view lim stack.

        For convenience of being directly connected as a GUI callback, which
        often get passed additional parameters, this method accepts arbitrary
        parameters, but does not use them.
        """
        self._nav_stack.back()
        self.set_history_buttons()
        self._update_view()

    def forward(self, *args):
        """
        Move forward in the view lim stack.

        For convenience of being directly connected as a GUI callback, which
        often get passed additional parameters, this method accepts arbitrary
        parameters, but does not use them.
        """
        self._nav_stack.forward()
        self.set_history_buttons()
        self._update_view()

    @_api.deprecated("3.3", alternative="__init__")
    def _init_toolbar(self):
        """
        This is where you actually build the GUI widgets (called by
        __init__).  The icons ``home.xpm``, ``back.xpm``, ``forward.xpm``,
        ``hand.xpm``, ``zoom_to_rect.xpm`` and ``filesave.xpm`` are standard
        across backends (there are ppm versions in CVS also).

        You just need to set the callbacks

        home         : self.home
        back         : self.back
        forward      : self.forward
        hand         : self.pan
        zoom_to_rect : self.zoom
        filesave     : self.save_figure

        You only need to define the last one - the others are in the base
        class implementation.

        """
        raise NotImplementedError

    def _update_cursor(self, event):
        """
        Update the cursor after a mouse move event or a tool (de)activation.
        """
        if not event.inaxes or not self.mode:
            if self._lastCursor != cursors.POINTER:
                self.set_cursor(cursors.POINTER)
                self._lastCursor = cursors.POINTER
        else:
            if (self.mode == _Mode.ZOOM
                    and self._lastCursor != cursors.SELECT_REGION):
                self.set_cursor(cursors.SELECT_REGION)
                self._lastCursor = cursors.SELECT_REGION
            elif (self.mode == _Mode.PAN
                  and self._lastCursor != cursors.MOVE):
                self.set_cursor(cursors.MOVE)
                self._lastCursor = cursors.MOVE

    @contextmanager
    def _wait_cursor_for_draw_cm(self):
        """
        Set the cursor to a wait cursor when drawing the canvas.

        In order to avoid constantly changing the cursor when the canvas
        changes frequently, do nothing if this context was triggered during the
        last second.  (Optimally we'd prefer only setting the wait cursor if
        the *current* draw takes too long, but the current draw blocks the GUI
        thread).
        """
        self._draw_time, last_draw_time = (
            time.time(), getattr(self, "_draw_time", -np.inf))
        if self._draw_time - last_draw_time > 1:
            try:
                self.set_cursor(cursors.WAIT)
                yield
            finally:
                self.set_cursor(self._lastCursor)
        else:
            yield

    @staticmethod
    def _mouse_event_to_message(event):
        if event.inaxes and event.inaxes.get_navigate():
            try:
                s = event.inaxes.format_coord(event.xdata, event.ydata)
            except (ValueError, OverflowError):
                pass
            else:
                s = s.rstrip()
                artists = [a for a in event.inaxes._mouseover_set
                           if a.contains(event)[0] and a.get_visible()]
                if artists:
                    a = cbook._topmost_artist(artists)
                    if a is not event.inaxes.patch:
                        data = a.get_cursor_data(event)
                        if data is not None:
                            data_str = a.format_cursor_data(data).rstrip()
                            if data_str:
                                s = s + '\n' + data_str
                return s

    def mouse_move(self, event):
        self._update_cursor(event)

        s = self._mouse_event_to_message(event)
        if s is not None:
            self.set_message(s)
        else:
            self.set_message(self.mode)

    def _zoom_pan_handler(self, event):
        if self.mode == _Mode.PAN:
            if event.name == "button_press_event":
                self.press_pan(event)
            elif event.name == "button_release_event":
                self.release_pan(event)
        if self.mode == _Mode.ZOOM:
            if event.name == "button_press_event":
                self.press_zoom(event)
            elif event.name == "button_release_event":
                self.release_zoom(event)

    @_api.deprecated("3.3")
    def press(self, event):
        """Called whenever a mouse button is pressed."""

    @_api.deprecated("3.3")
    def release(self, event):
        """Callback for mouse button release."""

    def pan(self, *args):
        """
        Toggle the pan/zoom tool.

        Pan with left button, zoom with right.
        """
        if self.mode == _Mode.PAN:
            self.mode = _Mode.NONE
            self.canvas.widgetlock.release(self)
        else:
            self.mode = _Mode.PAN
            self.canvas.widgetlock(self)
        for a in self.canvas.figure.get_axes():
            a.set_navigate_mode(self.mode._navigate_mode)
        self.set_message(self.mode)

    _PanInfo = namedtuple("_PanInfo", "button axes cid")

    def press_pan(self, event):
        """Callback for mouse button press in pan/zoom mode."""
        if (event.button not in [MouseButton.LEFT, MouseButton.RIGHT]
                or event.x is None or event.y is None):
            return
        axes = [a for a in self.canvas.figure.get_axes()
                if a.in_axes(event) and a.get_navigate() and a.can_pan()]
        if not axes:
            return
        if self._nav_stack() is None:
            self.push_current()  # set the home button to this view
        for ax in axes:
            ax.start_pan(event.x, event.y, event.button)
        self.canvas.mpl_disconnect(self._id_drag)
        id_drag = self.canvas.mpl_connect("motion_notify_event", self.drag_pan)
        self._pan_info = self._PanInfo(
            button=event.button, axes=axes, cid=id_drag)
        press = _api.deprecate_method_override(
            __class__.press, self, since="3.3", message="Calling an "
            "overridden press() at pan start is deprecated since %(since)s "
            "and will be removed %(removal)s; override press_pan() instead.")
        if press is not None:
            press(event)

    def drag_pan(self, event):
        """Callback for dragging in pan/zoom mode."""
        for ax in self._pan_info.axes:
            # Using the recorded button at the press is safer than the current
            # button, as multiple buttons can get pressed during motion.
            ax.drag_pan(self._pan_info.button, event.key, event.x, event.y)
        self.canvas.draw_idle()

    def release_pan(self, event):
        """Callback for mouse button release in pan/zoom mode."""
        if self._pan_info is None:
            return
        self.canvas.mpl_disconnect(self._pan_info.cid)
        self._id_drag = self.canvas.mpl_connect(
            'motion_notify_event', self.mouse_move)
        for ax in self._pan_info.axes:
            ax.end_pan()
        release = _api.deprecate_method_override(
            __class__.press, self, since="3.3", message="Calling an "
            "overridden release() at pan stop is deprecated since %(since)s "
            "and will be removed %(removal)s; override release_pan() instead.")
        if release is not None:
            release(event)
        self._draw()
        self._pan_info = None
        self.push_current()

    def zoom(self, *args):
        """Toggle zoom to rect mode."""
        if self.mode == _Mode.ZOOM:
            self.mode = _Mode.NONE
            self.canvas.widgetlock.release(self)
        else:
            self.mode = _Mode.ZOOM
            self.canvas.widgetlock(self)
        for a in self.canvas.figure.get_axes():
            a.set_navigate_mode(self.mode._navigate_mode)
        self.set_message(self.mode)

    _ZoomInfo = namedtuple("_ZoomInfo", "direction start_xy axes cid")

    def press_zoom(self, event):
        """Callback for mouse button press in zoom to rect mode."""
        if (event.button not in [MouseButton.LEFT, MouseButton.RIGHT]
                or event.x is None or event.y is None):
            return
        axes = [a for a in self.canvas.figure.get_axes()
                if a.in_axes(event) and a.get_navigate() and a.can_zoom()]
        if not axes:
            return
        if self._nav_stack() is None:
            self.push_current()  # set the home button to this view
        id_zoom = self.canvas.mpl_connect(
            "motion_notify_event", self.drag_zoom)
        self._zoom_info = self._ZoomInfo(
            direction="in" if event.button == 1 else "out",
            start_xy=(event.x, event.y), axes=axes, cid=id_zoom)
        press = _api.deprecate_method_override(
            __class__.press, self, since="3.3", message="Calling an "
            "overridden press() at zoom start is deprecated since %(since)s "
            "and will be removed %(removal)s; override press_zoom() instead.")
        if press is not None:
            press(event)

    def drag_zoom(self, event):
        """Callback for dragging in zoom mode."""
        start_xy = self._zoom_info.start_xy
        ax = self._zoom_info.axes[0]
        (x1, y1), (x2, y2) = np.clip(
            [start_xy, [event.x, event.y]], ax.bbox.min, ax.bbox.max)
        if event.key == "x":
            y1, y2 = ax.bbox.intervaly
        elif event.key == "y":
            x1, x2 = ax.bbox.intervalx
        self.draw_rubberband(event, x1, y1, x2, y2)

    def release_zoom(self, event):
        """Callback for mouse button release in zoom to rect mode."""
        if self._zoom_info is None:
            return

        # We don't check the event button here, so that zooms can be cancelled
        # by (pressing and) releasing another mouse button.
        self.canvas.mpl_disconnect(self._zoom_info.cid)
        self.remove_rubberband()

        start_x, start_y = self._zoom_info.start_xy
        # Ignore single clicks: 5 pixels is a threshold that allows the user to
        # "cancel" a zoom action by zooming by less than 5 pixels.
        if ((abs(event.x - start_x) < 5 and event.key != "y")
                or (abs(event.y - start_y) < 5 and event.key != "x")):
            self._draw()
            self._zoom_info = None
            release = _api.deprecate_method_override(
                __class__.press, self, since="3.3", message="Calling an "
                "overridden release() at zoom stop is deprecated since "
                "%(since)s and will be removed %(removal)s; override "
                "release_zoom() instead.")
            if release is not None:
                release(event)
            return

        for i, ax in enumerate(self._zoom_info.axes):
            # Detect whether this axes is twinned with an earlier axes in the
            # list of zoomed axes, to avoid double zooming.
            twinx = any(ax.get_shared_x_axes().joined(ax, prev)
                        for prev in self._zoom_info.axes[:i])
            twiny = any(ax.get_shared_y_axes().joined(ax, prev)
                        for prev in self._zoom_info.axes[:i])
            ax._set_view_from_bbox(
                (start_x, start_y, event.x, event.y),
                self._zoom_info.direction, event.key, twinx, twiny)

        self._draw()
        self._zoom_info = None
        self.push_current()

        release = _api.deprecate_method_override(
            __class__.release, self, since="3.3", message="Calling an "
            "overridden release() at zoom stop is deprecated since %(since)s "
            "and will be removed %(removal)s; override release_zoom() "
            "instead.")
        if release is not None:
            release(event)

    def push_current(self):
        """Push the current view limits and position onto the stack."""
        self._nav_stack.push(
            WeakKeyDictionary(
                {ax: (ax._get_view(),
                      # Store both the original and modified positions.
                      (ax.get_position(True).frozen(),
                       ax.get_position().frozen()))
                 for ax in self.canvas.figure.axes}))
        self.set_history_buttons()

    @_api.deprecated("3.3", alternative="toolbar.canvas.draw_idle()")
    def draw(self):
        """Redraw the canvases, update the locators."""
        self._draw()

    # Can be removed once Locator.refresh() is removed, and replaced by an
    # inline call to self.canvas.draw_idle().
    def _draw(self):
        for a in self.canvas.figure.get_axes():
            xaxis = getattr(a, 'xaxis', None)
            yaxis = getattr(a, 'yaxis', None)
            locators = []
            if xaxis is not None:
                locators.append(xaxis.get_major_locator())
                locators.append(xaxis.get_minor_locator())
            if yaxis is not None:
                locators.append(yaxis.get_major_locator())
                locators.append(yaxis.get_minor_locator())

            for loc in locators:
                mpl.ticker._if_refresh_overridden_call_and_emit_deprec(loc)
        self.canvas.draw_idle()

    def _update_view(self):
        """
        Update the viewlim and position from the view and position stack for
        each axes.
        """
        nav_info = self._nav_stack()
        if nav_info is None:
            return
        # Retrieve all items at once to avoid any risk of GC deleting an Axes
        # while in the middle of the loop below.
        items = list(nav_info.items())
        for ax, (view, (pos_orig, pos_active)) in items:
            ax._set_view(view)
            # Restore both the original and modified positions
            ax._set_position(pos_orig, 'original')
            ax._set_position(pos_active, 'active')
        self.canvas.draw_idle()

    def configure_subplots(self, *args):
        plt = _safe_pyplot_import()
        self.subplot_tool = plt.subplot_tool(self.canvas.figure)
        self.subplot_tool.figure.canvas.manager.show()

    def save_figure(self, *args):
        """Save the current figure."""
        raise NotImplementedError

    def set_cursor(self, cursor):
        """
        Set the current cursor to one of the :class:`Cursors` enums values.

        If required by the backend, this method should trigger an update in
        the backend event loop after the cursor is set, as this method may be
        called e.g. before a long-running task during which the GUI is not
        updated.
        """

    def update(self):
        """Reset the axes stack."""
        self._nav_stack.clear()
        self.set_history_buttons()

    def set_history_buttons(self):
        """Enable or disable the back/forward button."""

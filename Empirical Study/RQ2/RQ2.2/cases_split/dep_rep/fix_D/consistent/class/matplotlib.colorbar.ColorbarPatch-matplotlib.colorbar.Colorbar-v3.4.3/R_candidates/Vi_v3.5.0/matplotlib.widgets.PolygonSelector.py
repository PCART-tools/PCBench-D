class PolygonSelector(_SelectorWidget):
    """
    Select a polygon region of an axes.

    Place vertices with each mouse click, and make the selection by completing
    the polygon (clicking on the first vertex). Once drawn individual vertices
    can be moved by clicking and dragging with the left mouse button, or
    removed by clicking the right mouse button.

    In addition, the following modifier keys can be used:

    - Hold *ctrl* and click and drag a vertex to reposition it before the
      polygon has been completed.
    - Hold the *shift* key and click and drag anywhere in the axes to move
      all vertices.
    - Press the *esc* key to start a new polygon.

    For the selector to remain responsive you must keep a reference to it.

    Parameters
    ----------
    ax : `~matplotlib.axes.Axes`
        The parent axes for the widget.

    onselect : function
        When a polygon is completed or modified after completion,
        the *onselect* function is called and passed a list of the vertices as
        ``(xdata, ydata)`` tuples.

    useblit : bool, default: False
        Whether to use blitting for faster drawing (if supported by the
        backend).

    props : dict, optional
        Properties with which the line is drawn, see `matplotlib.lines.Line2D`
        for valid properties.
        Default:

            ``dict(color='k', linestyle='-', linewidth=2, alpha=0.5)``

    handle_props : dict, optional
        Artist properties for the markers drawn at the vertices of the polygon.
        See the marker arguments in `matplotlib.lines.Line2D` for valid
        properties.  Default values are defined in ``mpl.rcParams`` except for
        the default value of ``markeredgecolor`` which will be the same as the
        ``color`` property in *props*.

    grab_range : float, default: 10
        A vertex is selected (to complete the polygon or to move a vertex) if
        the mouse click is within *grab_range* pixels of the vertex.

    Examples
    --------
    :doc:`/gallery/widgets/polygon_selector_demo`

    Notes
    -----
    If only one point remains after removing points, the selector reverts to an
    incomplete state and you can start drawing a new polygon from the existing
    point.
    """

    @_api.rename_parameter("3.5", "lineprops", "props")
    @_api.rename_parameter("3.5", "markerprops", "handle_props")
    @_api.rename_parameter("3.5", "vertex_select_radius", "grab_range")
    def __init__(self, ax, onselect, useblit=False,
                 props=None, handle_props=None, grab_range=10):
        # The state modifiers 'move', 'square', and 'center' are expected by
        # _SelectorWidget but are not supported by PolygonSelector
        # Note: could not use the existing 'move' state modifier in-place of
        # 'move_all' because _SelectorWidget automatically discards 'move'
        # from the state on button release.
        state_modifier_keys = dict(clear='escape', move_vertex='control',
                                   move_all='shift', move='not-applicable',
                                   square='not-applicable',
                                   center='not-applicable')
        super().__init__(ax, onselect, useblit=useblit,
                         state_modifier_keys=state_modifier_keys)

        self._xs, self._ys = [0], [0]

        if props is None:
            props = dict(color='k', linestyle='-', linewidth=2, alpha=0.5)
        props['animated'] = self.useblit
        self._props = props
        line = Line2D(self._xs, self._ys, **self._props)
        self.ax.add_line(line)
        self._selection_artist = line

        if handle_props is None:
            handle_props = dict(markeredgecolor='k',
                                markerfacecolor=self._props.get('color', 'k'))
        self._handle_props = handle_props
        self._polygon_handles = ToolHandles(self.ax, self._xs, self._ys,
                                            useblit=self.useblit,
                                            marker_props=self._handle_props)

        self._active_handle_idx = -1
        self.grab_range = grab_range

        self.set_visible(True)

    line = _api.deprecated("3.5")(
        property(lambda self: self._selection_artist)
        )

    vertex_select_radius = _api.deprecated("3.5", name="vertex_select_radius",
                                           alternative="grab_range")(
        property(lambda self: self.grab_range,
                 lambda self, value: setattr(self, "grab_range", value))
        )

    @property
    def _nverts(self):
        return len(self._xs)

    @property
    def _handles_artists(self):
        return self._polygon_handles.artists

    def _remove_vertex(self, i):
        """Remove vertex with index i."""
        if (self._nverts > 2 and
                self._selection_completed and
                i in (0, self._nverts - 1)):
            # If selecting the first or final vertex, remove both first and
            # last vertex as they are the same for a closed polygon
            self._xs.pop(0)
            self._ys.pop(0)
            self._xs.pop(-1)
            self._ys.pop(-1)
            # Close the polygon again by appending the new first vertex to the
            # end
            self._xs.append(self._xs[0])
            self._ys.append(self._ys[0])
        else:
            self._xs.pop(i)
            self._ys.pop(i)
        if self._nverts <= 2:
            # If only one point left, return to incomplete state to let user
            # start drawing again
            self._selection_completed = False

    def _press(self, event):
        """Button press event handler."""
        # Check for selection of a tool handle.
        if ((self._selection_completed or 'move_vertex' in self._state)
                and len(self._xs) > 0):
            h_idx, h_dist = self._polygon_handles.closest(event.x, event.y)
            if h_dist < self.grab_range:
                self._active_handle_idx = h_idx
        # Save the vertex positions at the time of the press event (needed to
        # support the 'move_all' state modifier).
        self._xs_at_press, self._ys_at_press = self._xs.copy(), self._ys.copy()

    def _release(self, event):
        """Button release event handler."""
        # Release active tool handle.
        if self._active_handle_idx >= 0:
            if event.button == 3:
                self._remove_vertex(self._active_handle_idx)
                self._draw_polygon()
            self._active_handle_idx = -1

        # Complete the polygon.
        elif (len(self._xs) > 3
              and self._xs[-1] == self._xs[0]
              and self._ys[-1] == self._ys[0]):
            self._selection_completed = True

        # Place new vertex.
        elif (not self._selection_completed
              and 'move_all' not in self._state
              and 'move_vertex' not in self._state):
            self._xs.insert(-1, event.xdata)
            self._ys.insert(-1, event.ydata)

        if self._selection_completed:
            self.onselect(self.verts)

    def onmove(self, event):
        """Cursor move event handler and validator."""
        # Method overrides _SelectorWidget.onmove because the polygon selector
        # needs to process the move callback even if there is no button press.
        # _SelectorWidget.onmove include logic to ignore move event if
        # _eventpress is None.
        if not self.ignore(event):
            event = self._clean_event(event)
            self._onmove(event)
            return True
        return False

    def _onmove(self, event):
        """Cursor move event handler."""
        # Move the active vertex (ToolHandle).
        if self._active_handle_idx >= 0:
            idx = self._active_handle_idx
            self._xs[idx], self._ys[idx] = event.xdata, event.ydata
            # Also update the end of the polygon line if the first vertex is
            # the active handle and the polygon is completed.
            if idx == 0 and self._selection_completed:
                self._xs[-1], self._ys[-1] = event.xdata, event.ydata

        # Move all vertices.
        elif 'move_all' in self._state and self._eventpress:
            dx = event.xdata - self._eventpress.xdata
            dy = event.ydata - self._eventpress.ydata
            for k in range(len(self._xs)):
                self._xs[k] = self._xs_at_press[k] + dx
                self._ys[k] = self._ys_at_press[k] + dy

        # Do nothing if completed or waiting for a move.
        elif (self._selection_completed
              or 'move_vertex' in self._state or 'move_all' in self._state):
            return

        # Position pending vertex.
        else:
            # Calculate distance to the start vertex.
            x0, y0 = self._selection_artist.get_transform().transform(
                    (self._xs[0], self._ys[0])
                )
            v0_dist = np.hypot(x0 - event.x, y0 - event.y)
            # Lock on to the start vertex if near it and ready to complete.
            if len(self._xs) > 3 and v0_dist < self.grab_range:
                self._xs[-1], self._ys[-1] = self._xs[0], self._ys[0]
            else:
                self._xs[-1], self._ys[-1] = event.xdata, event.ydata

        self._draw_polygon()

    def _on_key_press(self, event):
        """Key press event handler."""
        # Remove the pending vertex if entering the 'move_vertex' or
        # 'move_all' mode
        if (not self._selection_completed
                and ('move_vertex' in self._state or
                     'move_all' in self._state)):
            self._xs, self._ys = self._xs[:-1], self._ys[:-1]
            self._draw_polygon()

    def _on_key_release(self, event):
        """Key release event handler."""
        # Add back the pending vertex if leaving the 'move_vertex' or
        # 'move_all' mode (by checking the released key)
        if (not self._selection_completed
                and
                (event.key == self.state_modifier_keys.get('move_vertex')
                 or event.key == self.state_modifier_keys.get('move_all'))):
            self._xs.append(event.xdata)
            self._ys.append(event.ydata)
            self._draw_polygon()
        # Reset the polygon if the released key is the 'clear' key.
        elif event.key == self.state_modifier_keys.get('clear'):
            event = self._clean_event(event)
            self._xs, self._ys = [event.xdata], [event.ydata]
            self._selection_completed = False
            self.set_visible(True)

    def _draw_polygon(self):
        """Redraw the polygon based on the new vertex positions."""
        self._selection_artist.set_data(self._xs, self._ys)
        # Only show one tool handle at the start and end vertex of the polygon
        # if the polygon is completed or the user is locked on to the start
        # vertex.
        if (self._selection_completed
                or (len(self._xs) > 3
                    and self._xs[-1] == self._xs[0]
                    and self._ys[-1] == self._ys[0])):
            self._polygon_handles.set_data(self._xs[:-1], self._ys[:-1])
        else:
            self._polygon_handles.set_data(self._xs, self._ys)
        self.update()

    @property
    def verts(self):
        """The polygon vertices, as a list of ``(x, y)`` pairs."""
        return list(zip(self._xs[:-1], self._ys[:-1]))

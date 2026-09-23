    def __init__(self, ax, onselect, drawtype='box',
                 minspanx=None, minspany=None, useblit=False,
                 lineprops=None, rectprops=None, spancoords='data',
                 button=None, maxdist=10, marker_props=None,
                 interactive=False, state_modifier_keys=None):

        """
        Create a selector in *ax*.  When a selection is made, clear
        the span and call onselect with::

          onselect(pos_1, pos_2)

        and clear the drawn box/line. The ``pos_1`` and ``pos_2`` are
        arrays of length 2 containing the x- and y-coordinate.

        If *minspanx* is not *None* then events smaller than *minspanx*
        in x direction are ignored (it's the same for y).

        The rectangle is drawn with *rectprops*; default::

          rectprops = dict(facecolor='red', edgecolor = 'black',
                           alpha=0.2, fill=True)

        The line is drawn with *lineprops*; default::

          lineprops = dict(color='black', linestyle='-',
                           linewidth = 2, alpha=0.5)

        Use *drawtype* if you want the mouse to draw a line,
        a box or nothing between click and actual position by setting

        ``drawtype = 'line'``, ``drawtype='box'`` or ``drawtype = 'none'``.

        *spancoords* is one of 'data' or 'pixels'.  If 'data', *minspanx*
        and *minspanx* will be interpreted in the same coordinates as
        the x and y axis. If 'pixels', they are in pixels.

        *button* is a list of integers indicating which mouse buttons should
        be used for rectangle selection.  You can also specify a single
        integer if only a single button is desired.  Default is *None*,
        which does not limit which button can be used.

        Note, typically:
         1 = left mouse button
         2 = center mouse button (scroll wheel)
         3 = right mouse button

        *interactive* will draw a set of handles and allow you interact
        with the widget after it is drawn.

        *state_modifier_keys* are keyboard modifiers that affect the behavior
        of the widget.

        The defaults are:
        dict(move=' ', clear='escape', square='shift', center='ctrl')

        Keyboard modifiers, which:
        'move': Move the existing shape.
        'clear': Clear the current shape.
        'square': Makes the shape square.
        'center': Make the initial point the center of the shape.
        'square' and 'center' can be combined.
        """
        _SelectorWidget.__init__(self, ax, onselect, useblit=useblit,
                                 button=button,
                                 state_modifier_keys=state_modifier_keys)

        self.to_draw = None
        self.visible = True
        self.interactive = interactive

        if drawtype == 'none':
            drawtype = 'line'                        # draw a line but make it
            self.visible = False                     # invisible

        if drawtype == 'box':
            if rectprops is None:
                rectprops = dict(facecolor='red', edgecolor='black',
                                 alpha=0.2, fill=True)
            rectprops['animated'] = self.useblit
            self.rectprops = rectprops
            self.to_draw = self._shape_klass((0, 0), 0, 1, visible=False,
                                             **self.rectprops)
            self.ax.add_patch(self.to_draw)
        if drawtype == 'line':
            if lineprops is None:
                lineprops = dict(color='black', linestyle='-',
                                 linewidth=2, alpha=0.5)
            lineprops['animated'] = self.useblit
            self.lineprops = lineprops
            self.to_draw = Line2D([0, 0], [0, 0], visible=False,
                                  **self.lineprops)
            self.ax.add_line(self.to_draw)

        self.minspanx = minspanx
        self.minspany = minspany

        if spancoords not in ('data', 'pixels'):
            msg = "'spancoords' must be one of [ 'data' | 'pixels' ]"
            raise ValueError(msg)

        self.spancoords = spancoords
        self.drawtype = drawtype

        self.maxdist = maxdist

        if rectprops is None:
            props = dict(mec='r')
        else:
            props = dict(mec=rectprops.get('edgecolor', 'r'))
        self._corner_order = ['NW', 'NE', 'SE', 'SW']
        xc, yc = self.corners
        self._corner_handles = ToolHandles(self.ax, xc, yc, marker_props=props,
                                           useblit=self.useblit)

        self._edge_order = ['W', 'N', 'E', 'S']
        xe, ye = self.edge_centers
        self._edge_handles = ToolHandles(self.ax, xe, ye, marker='s',
                                         marker_props=props,
                                         useblit=self.useblit)

        xc, yc = self.center
        self._center_handle = ToolHandles(self.ax, [xc], [yc], marker='s',
                                          marker_props=props,
                                          useblit=self.useblit)

        self.active_handle = None

        self.artists = [self.to_draw, self._center_handle.artist,
                        self._corner_handles.artist,
                        self._edge_handles.artist]

        if not self.interactive:
            self.artists = [self.to_draw]

        self._extents_on_press = None

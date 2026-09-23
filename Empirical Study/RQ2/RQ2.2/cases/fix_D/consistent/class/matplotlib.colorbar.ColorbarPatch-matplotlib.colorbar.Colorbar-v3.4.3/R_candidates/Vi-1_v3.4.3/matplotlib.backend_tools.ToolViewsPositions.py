class ToolViewsPositions(ToolBase):
    """
    Auxiliary Tool to handle changes in views and positions.

    Runs in the background and should get used by all the tools that
    need to access the figure's history of views and positions, e.g.

    * `ToolZoom`
    * `ToolPan`
    * `ToolHome`
    * `ToolBack`
    * `ToolForward`
    """

    def __init__(self, *args, **kwargs):
        self.views = WeakKeyDictionary()
        self.positions = WeakKeyDictionary()
        self.home_views = WeakKeyDictionary()
        super().__init__(*args, **kwargs)

    def add_figure(self, figure):
        """Add the current figure to the stack of views and positions."""

        if figure not in self.views:
            self.views[figure] = cbook.Stack()
            self.positions[figure] = cbook.Stack()
            self.home_views[figure] = WeakKeyDictionary()
            # Define Home
            self.push_current(figure)
            # Make sure we add a home view for new axes as they're added
            figure.add_axobserver(lambda fig: self.update_home_views(fig))

    def clear(self, figure):
        """Reset the axes stack."""
        if figure in self.views:
            self.views[figure].clear()
            self.positions[figure].clear()
            self.home_views[figure].clear()
            self.update_home_views()

    def update_view(self):
        """
        Update the view limits and position for each axes from the current
        stack position. If any axes are present in the figure that aren't in
        the current stack position, use the home view limits for those axes and
        don't update *any* positions.
        """

        views = self.views[self.figure]()
        if views is None:
            return
        pos = self.positions[self.figure]()
        if pos is None:
            return
        home_views = self.home_views[self.figure]
        all_axes = self.figure.get_axes()
        for a in all_axes:
            if a in views:
                cur_view = views[a]
            else:
                cur_view = home_views[a]
            a._set_view(cur_view)

        if set(all_axes).issubset(pos):
            for a in all_axes:
                # Restore both the original and modified positions
                a._set_position(pos[a][0], 'original')
                a._set_position(pos[a][1], 'active')

        self.figure.canvas.draw_idle()

    def push_current(self, figure=None):
        """
        Push the current view limits and position onto their respective stacks.
        """
        if not figure:
            figure = self.figure
        views = WeakKeyDictionary()
        pos = WeakKeyDictionary()
        for a in figure.get_axes():
            views[a] = a._get_view()
            pos[a] = self._axes_pos(a)
        self.views[figure].push(views)
        self.positions[figure].push(pos)

    def _axes_pos(self, ax):
        """
        Return the original and modified positions for the specified axes.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The `.Axes` to get the positions for.

        Returns
        -------
        original_position, modified_position
            A tuple of the original and modified positions.
        """

        return (ax.get_position(True).frozen(),
                ax.get_position().frozen())

    def update_home_views(self, figure=None):
        """
        Make sure that ``self.home_views`` has an entry for all axes present
        in the figure.
        """

        if not figure:
            figure = self.figure
        for a in figure.get_axes():
            if a not in self.home_views[figure]:
                self.home_views[figure][a] = a._get_view()

    @_api.deprecated("3.3", alternative="self.figure.canvas.draw_idle()")
    def refresh_locators(self):
        """Redraw the canvases, update the locators."""
        self._refresh_locators()

    # Can be removed once Locator.refresh() is removed, and replaced by an
    # inline call to self.figure.canvas.draw_idle().
    def _refresh_locators(self):
        for a in self.figure.get_axes():
            xaxis = getattr(a, 'xaxis', None)
            yaxis = getattr(a, 'yaxis', None)
            zaxis = getattr(a, 'zaxis', None)
            locators = []
            if xaxis is not None:
                locators.append(xaxis.get_major_locator())
                locators.append(xaxis.get_minor_locator())
            if yaxis is not None:
                locators.append(yaxis.get_major_locator())
                locators.append(yaxis.get_minor_locator())
            if zaxis is not None:
                locators.append(zaxis.get_major_locator())
                locators.append(zaxis.get_minor_locator())

            for loc in locators:
                mpl.ticker._if_refresh_overridden_call_and_emit_deprec(loc)
        self.figure.canvas.draw_idle()

    def home(self):
        """Recall the first view and position from the stack."""
        self.views[self.figure].home()
        self.positions[self.figure].home()

    def back(self):
        """Back one step in the stack of views and positions."""
        self.views[self.figure].back()
        self.positions[self.figure].back()

    def forward(self):
        """Forward one step in the stack of views and positions."""
        self.views[self.figure].forward()
        self.positions[self.figure].forward()

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

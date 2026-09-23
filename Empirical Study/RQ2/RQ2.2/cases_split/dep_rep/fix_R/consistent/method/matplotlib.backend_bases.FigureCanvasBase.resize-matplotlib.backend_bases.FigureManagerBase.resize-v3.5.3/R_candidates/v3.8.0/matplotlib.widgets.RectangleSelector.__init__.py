    def __init__(self, ax, onselect, *, minspanx=0, minspany=0, useblit=False,
                 props=None, spancoords='data', button=None, grab_range=10,
                 handle_props=None, interactive=False,
                 state_modifier_keys=None, drag_from_anywhere=False,
                 ignore_event_outside=False, use_data_coordinates=False):
        super().__init__(ax, onselect, useblit=useblit, button=button,
                         state_modifier_keys=state_modifier_keys,
                         use_data_coordinates=use_data_coordinates)

        self._interactive = interactive
        self.drag_from_anywhere = drag_from_anywhere
        self.ignore_event_outside = ignore_event_outside
        self._rotation = 0.0
        self._aspect_ratio_correction = 1.0

        # State to allow the option of an interactive selector that can't be
        # interactively drawn. This is used in PolygonSelector as an
        # interactive bounding box to allow the polygon to be easily resized
        self._allow_creation = True

        if props is None:
            props = dict(facecolor='red', edgecolor='black',
                         alpha=0.2, fill=True)
        props = {**props, 'animated': self.useblit}
        self._visible = props.pop('visible', self._visible)
        to_draw = self._init_shape(**props)
        self.ax.add_patch(to_draw)

        self._selection_artist = to_draw
        self._set_aspect_ratio_correction()

        self.minspanx = minspanx
        self.minspany = minspany

        _api.check_in_list(['data', 'pixels'], spancoords=spancoords)
        self.spancoords = spancoords

        self.grab_range = grab_range

        if self._interactive:
            self._handle_props = {
                'markeredgecolor': (props or {}).get('edgecolor', 'black'),
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

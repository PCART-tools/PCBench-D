    @_api.rename_parameter("3.5", "lineprops", "props")
    @_api.rename_parameter("3.5", "markerprops", "handle_props")
    @_api.rename_parameter("3.5", "vertex_select_radius", "grab_range")
    def __init__(self, ax, onselect, useblit=False,
                 props=None, handle_props=None, grab_range=10, *,
                 draw_bounding_box=False, box_handle_props=None,
                 box_props=None):
        # The state modifiers 'move', 'square', and 'center' are expected by
        # _SelectorWidget but are not supported by PolygonSelector
        # Note: could not use the existing 'move' state modifier in-place of
        # 'move_all' because _SelectorWidget automatically discards 'move'
        # from the state on button release.
        state_modifier_keys = dict(clear='escape', move_vertex='control',
                                   move_all='shift', move='not-applicable',
                                   square='not-applicable',
                                   center='not-applicable',
                                   rotate='not-applicable')
        super().__init__(ax, onselect, useblit=useblit,
                         state_modifier_keys=state_modifier_keys)

        self._xys = [(0, 0)]

        if props is None:
            props = dict(color='k', linestyle='-', linewidth=2, alpha=0.5)
        props['animated'] = self.useblit
        self._props = props
        self._selection_artist = line = Line2D([], [], **self._props)
        self.ax.add_line(line)

        if handle_props is None:
            handle_props = dict(markeredgecolor='k',
                                markerfacecolor=self._props.get('color', 'k'))
        self._handle_props = handle_props
        self._polygon_handles = ToolHandles(self.ax, [], [],
                                            useblit=self.useblit,
                                            marker_props=self._handle_props)

        self._active_handle_idx = -1
        self.grab_range = grab_range

        self.set_visible(True)
        self._draw_box = draw_bounding_box
        self._box = None

        if box_handle_props is None:
            box_handle_props = {}
        self._box_handle_props = self._handle_props.update(box_handle_props)
        self._box_props = box_props

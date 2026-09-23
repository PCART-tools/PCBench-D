    def __init__(self, ax, onselect, direction, *, minspan=0, useblit=False,
                 props=None, onmove_callback=None, interactive=False,
                 button=None, handle_props=None, grab_range=10,
                 state_modifier_keys=None, drag_from_anywhere=False,
                 ignore_event_outside=False, snap_values=None):

        if state_modifier_keys is None:
            state_modifier_keys = dict(clear='escape',
                                       square='not-applicable',
                                       center='not-applicable',
                                       rotate='not-applicable')
        super().__init__(ax, onselect, useblit=useblit, button=button,
                         state_modifier_keys=state_modifier_keys)

        if props is None:
            props = dict(facecolor='red', alpha=0.5)

        props['animated'] = self.useblit

        self.direction = direction
        self._extents_on_press = None
        self.snap_values = snap_values

        self.onmove_callback = onmove_callback
        self.minspan = minspan

        self.grab_range = grab_range
        self._interactive = interactive
        self._edge_handles = None
        self.drag_from_anywhere = drag_from_anywhere
        self.ignore_event_outside = ignore_event_outside

        self.new_axes(ax, _props=props, _init=True)

        # Setup handles
        self._handle_props = {
            'color': props.get('facecolor', 'r'),
            **cbook.normalize_kwargs(handle_props, Line2D)}

        if self._interactive:
            self._edge_order = ['min', 'max']
            self._setup_edge_handles(self._handle_props)

        self._active_handle = None

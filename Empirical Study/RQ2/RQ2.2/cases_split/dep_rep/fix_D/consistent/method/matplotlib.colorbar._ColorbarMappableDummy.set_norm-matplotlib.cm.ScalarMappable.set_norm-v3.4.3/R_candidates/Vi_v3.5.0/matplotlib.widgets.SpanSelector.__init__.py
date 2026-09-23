    @_api.rename_parameter("3.5", "rectprops", "props")
    @_api.rename_parameter("3.5", "span_stays", "interactive")
    def __init__(self, ax, onselect, direction, minspan=0, useblit=False,
                 props=None, onmove_callback=None, interactive=False,
                 button=None, handle_props=None, grab_range=10,
                 drag_from_anywhere=False, ignore_event_outside=False):

        super().__init__(ax, onselect, useblit=useblit, button=button)

        if props is None:
            props = dict(facecolor='red', alpha=0.5)

        props['animated'] = self.useblit

        self.direction = direction

        self.visible = True
        self._extents_on_press = None

        # self._pressv is deprecated and we don't use it internally anymore
        # but we maintain it until it is removed
        self._pressv = None

        self._props = props
        self.onmove_callback = onmove_callback
        self.minspan = minspan

        self.grab_range = grab_range
        self._interactive = interactive
        self._edge_handles = None
        self.drag_from_anywhere = drag_from_anywhere
        self.ignore_event_outside = ignore_event_outside

        # Reset canvas so that `new_axes` connects events.
        self.canvas = None
        self.new_axes(ax)

        # Setup handles
        self._handle_props = {
            'color': props.get('facecolor', 'r'),
            **cbook.normalize_kwargs(handle_props, Line2D)}

        if self._interactive:
            self._edge_order = ['min', 'max']
            self._setup_edge_handles(self._handle_props)

        self._active_handle = None

        # prev attribute is deprecated but we still need to maintain it
        self._prev = (0, 0)

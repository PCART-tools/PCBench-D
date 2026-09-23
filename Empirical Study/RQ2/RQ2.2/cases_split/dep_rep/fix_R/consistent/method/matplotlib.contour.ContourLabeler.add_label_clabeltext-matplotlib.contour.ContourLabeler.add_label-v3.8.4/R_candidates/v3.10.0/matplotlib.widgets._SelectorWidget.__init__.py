    def __init__(self, ax, onselect=None, useblit=False, button=None,
                 state_modifier_keys=None, use_data_coordinates=False):
        super().__init__(ax)

        self._visible = True
        if onselect is None:
            self.onselect = lambda *args: None
        else:
            self.onselect = onselect
        self.useblit = useblit and self.canvas.supports_blit
        self.connect_default_events()

        self._state_modifier_keys = dict(move=' ', clear='escape',
                                         square='shift', center='control',
                                         rotate='r')
        self._state_modifier_keys.update(state_modifier_keys or {})
        self._use_data_coordinates = use_data_coordinates

        self.background = None

        if isinstance(button, Integral):
            self.validButtons = [button]
        else:
            self.validButtons = button

        # Set to True when a selection is completed, otherwise is False
        self._selection_completed = False

        # will save the data (position at mouseclick)
        self._eventpress = None
        # will save the data (pos. at mouserelease)
        self._eventrelease = None
        self._prev_event = None
        self._state = set()

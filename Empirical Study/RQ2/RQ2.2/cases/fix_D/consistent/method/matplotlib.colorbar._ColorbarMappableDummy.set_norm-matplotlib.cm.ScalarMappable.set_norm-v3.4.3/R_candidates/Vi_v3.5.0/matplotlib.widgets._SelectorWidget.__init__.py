    def __init__(self, ax, onselect, useblit=False, button=None,
                 state_modifier_keys=None):
        super().__init__(ax)

        self.visible = True
        self.onselect = onselect
        self.useblit = useblit and self.canvas.supports_blit
        self.connect_default_events()

        self.state_modifier_keys = dict(move=' ', clear='escape',
                                        square='shift', center='control')
        self.state_modifier_keys.update(state_modifier_keys or {})

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
        self._default_state = set()

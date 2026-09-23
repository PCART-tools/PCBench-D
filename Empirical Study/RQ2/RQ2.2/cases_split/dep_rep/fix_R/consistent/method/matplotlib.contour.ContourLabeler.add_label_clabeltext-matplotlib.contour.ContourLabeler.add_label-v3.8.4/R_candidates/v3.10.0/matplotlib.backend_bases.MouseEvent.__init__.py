    def __init__(self, name, canvas, x, y, button=None, key=None,
                 step=0, dblclick=False, guiEvent=None, *,
                 buttons=None, modifiers=None):
        super().__init__(
            name, canvas, x, y, guiEvent=guiEvent, modifiers=modifiers)
        if button in MouseButton.__members__.values():
            button = MouseButton(button)
        if name == "scroll_event" and button is None:
            if step > 0:
                button = "up"
            elif step < 0:
                button = "down"
        self.button = button
        if name == "motion_notify_event":
            self.buttons = frozenset(buttons if buttons is not None else [])
        else:
            # We don't support 'buttons' for button_press/release_event because
            # toolkits are inconsistent as to whether they report the state
            # before or after the event.
            if buttons:
                raise ValueError(
                    "'buttons' is only supported for 'motion_notify_event'")
            self.buttons = None
        self.key = key
        self.step = step
        self.dblclick = dblclick

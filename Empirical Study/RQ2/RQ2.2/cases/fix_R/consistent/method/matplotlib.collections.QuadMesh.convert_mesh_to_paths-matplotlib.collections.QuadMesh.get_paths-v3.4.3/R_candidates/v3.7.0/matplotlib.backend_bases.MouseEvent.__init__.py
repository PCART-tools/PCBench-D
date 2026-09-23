    def __init__(self, name, canvas, x, y, button=None, key=None,
                 step=0, dblclick=False, guiEvent=None, *, modifiers=None):
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
        self.key = key
        self.step = step
        self.dblclick = dblclick

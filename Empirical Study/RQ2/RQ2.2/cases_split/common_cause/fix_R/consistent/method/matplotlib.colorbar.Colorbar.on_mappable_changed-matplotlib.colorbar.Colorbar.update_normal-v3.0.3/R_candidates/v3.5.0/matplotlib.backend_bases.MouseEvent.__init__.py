    def __init__(self, name, canvas, x, y, button=None, key=None,
                 step=0, dblclick=False, guiEvent=None):
        if button in MouseButton.__members__.values():
            button = MouseButton(button)
        self.button = button
        self.key = key
        self.step = step
        self.dblclick = dblclick

        # super-init is deferred to the end because it calls back on
        # 'axes_enter_event', which requires a fully initialized event.
        super().__init__(name, canvas, x, y, guiEvent=guiEvent)

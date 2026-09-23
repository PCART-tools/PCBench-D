    def __init__(self, fig,
                 mouse_add=MouseButton.LEFT,
                 mouse_pop=MouseButton.RIGHT,
                 mouse_stop=MouseButton.MIDDLE):
        super().__init__(fig=fig,
                         eventslist=('button_press_event', 'key_press_event'))
        self.button_add = mouse_add
        self.button_pop = mouse_pop
        self.button_stop = mouse_stop

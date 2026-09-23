    def __init__(self, fig, mouse_add=1, mouse_pop=3, mouse_stop=2):
        BlockingInput.__init__(self, fig=fig,
                               eventslist=('button_press_event',
                                           'key_press_event'))
        self.button_add = mouse_add
        self.button_pop = mouse_pop
        self.button_stop = mouse_stop

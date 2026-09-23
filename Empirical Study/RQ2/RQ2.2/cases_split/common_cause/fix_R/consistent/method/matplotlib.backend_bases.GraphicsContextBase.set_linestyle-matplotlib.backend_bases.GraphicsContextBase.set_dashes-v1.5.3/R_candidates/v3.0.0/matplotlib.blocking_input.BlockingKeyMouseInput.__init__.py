    def __init__(self, fig):
        BlockingInput.__init__(self, fig=fig, eventslist=(
            'button_press_event', 'key_press_event'))

    def key_event(self):
        '''
        Process a key click event.  This maps certain keys to appropriate
        mouse click events.
        '''

        event = self.events[-1]
        if event.key is None:
            # at least in mac os X gtk backend some key returns None.
            return

        key = event.key.lower()

        if key in ['backspace', 'delete']:
            self.mouse_event_pop(event)
        elif key in ['escape', 'enter']:
            # on windows XP and wxAgg, the enter key doesn't seem to register
            self.mouse_event_stop(event)
        else:
            self.mouse_event_add(event)

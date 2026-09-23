    def press(self, event):
        """Button press handler and validator"""
        if not self.ignore(event):
            event = self._clean_event(event)
            self.eventpress = event
            self._prev_event = event
            key = event.key or ''
            key = key.replace('ctrl', 'control')
            # move state is locked in on a button press
            if key == self.state_modifier_keys['move']:
                self.state.add('move')
            self._press(event)
            return True
        return False

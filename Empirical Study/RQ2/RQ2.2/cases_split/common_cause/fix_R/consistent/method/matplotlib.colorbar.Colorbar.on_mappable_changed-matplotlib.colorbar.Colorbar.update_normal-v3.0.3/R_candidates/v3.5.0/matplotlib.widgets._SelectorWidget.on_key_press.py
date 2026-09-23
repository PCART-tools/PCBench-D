    def on_key_press(self, event):
        """Key press event handler and validator for all selection widgets."""
        if self.active:
            key = event.key or ''
            key = key.replace('ctrl', 'control')
            if key == self.state_modifier_keys['clear']:
                self.clear()
                return
            for (state, modifier) in self.state_modifier_keys.items():
                if modifier in key:
                    self._state.add(state)
            self._on_key_press(event)

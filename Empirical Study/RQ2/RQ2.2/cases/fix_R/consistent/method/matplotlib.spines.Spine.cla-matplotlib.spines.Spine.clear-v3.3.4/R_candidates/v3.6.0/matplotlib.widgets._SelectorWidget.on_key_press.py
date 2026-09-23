    def on_key_press(self, event):
        """Key press event handler and validator for all selection widgets."""
        if self.active:
            key = event.key or ''
            key = key.replace('ctrl', 'control')
            if key == self._state_modifier_keys['clear']:
                self.clear()
                return
            for (state, modifier) in self._state_modifier_keys.items():
                if modifier in key.split('+'):
                    # 'rotate' is changing _state on press and is not removed
                    # from _state when releasing
                    if state == 'rotate':
                        if state in self._state:
                            self._state.discard(state)
                        else:
                            self._state.add(state)
                    else:
                        self._state.add(state)
            self._on_key_press(event)

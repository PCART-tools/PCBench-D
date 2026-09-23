    def key_press_event(self, controller, keyval, keycode, state):
        KeyEvent(
            "key_press_event", self, self._get_key(keyval, keycode, state),
            *self._mpl_coords(),
            guiEvent=controller.get_current_event(),
        )._process()
        return True

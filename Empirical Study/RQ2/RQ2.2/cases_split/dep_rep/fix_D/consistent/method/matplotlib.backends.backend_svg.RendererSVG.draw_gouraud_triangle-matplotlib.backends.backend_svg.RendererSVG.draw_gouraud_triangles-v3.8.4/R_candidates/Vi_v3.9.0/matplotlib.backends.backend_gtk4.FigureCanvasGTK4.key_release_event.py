    def key_release_event(self, controller, keyval, keycode, state):
        KeyEvent(
            "key_release_event", self, self._get_key(keyval, keycode, state),
            *self._mpl_coords(),
        )._process()
        return True

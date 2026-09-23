    def key_press_event(self, controller, keyval, keycode, state):
        key = self._get_key(keyval, keycode, state)
        FigureCanvasBase.key_press_event(self, key)
        return True

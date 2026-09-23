    def mouse_move(self, event):
        self._update_cursor(event)

        s = self._mouse_event_to_message(event)
        if s is not None:
            self.set_message(s)
        else:
            self.set_message(self.mode)

    def set_history_buttons(self):
        can_backward = self._nav_stack._pos > 0
        can_forward = self._nav_stack._pos < len(self._nav_stack) - 1
        self.canvas.send_event('history_buttons',
                               Back=can_backward, Forward=can_forward)

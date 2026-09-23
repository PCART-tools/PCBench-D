    def set_history_buttons(self):
        state_map = {True: tk.NORMAL, False: tk.DISABLED}
        can_back = self._nav_stack._pos > 0
        can_forward = self._nav_stack._pos < len(self._nav_stack) - 1
        if "Back" in self._buttons:
            self._buttons['Back']['state'] = state_map[can_back]
        if "Forward" in self._buttons:
            self._buttons['Forward']['state'] = state_map[can_forward]

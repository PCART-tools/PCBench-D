    def set_history_buttons(self):
        if self._nav_stack._pos > 0:
            self._buttons['Back']['state'] = tk.NORMAL
        else:
            self._buttons['Back']['state'] = tk.DISABLED
        if self._nav_stack._pos < len(self._nav_stack._elements) - 1:
            self._buttons['Forward']['state'] = tk.NORMAL
        else:
            self._buttons['Forward']['state'] = tk.DISABLED

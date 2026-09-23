    def set_history_buttons(self):
        can_backward = self._nav_stack._pos > 0
        can_forward = self._nav_stack._pos < len(self._nav_stack) - 1
        if 'Back' in self.wx_ids:
            self.EnableTool(self.wx_ids['Back'], can_backward)
        if 'Forward' in self.wx_ids:
            self.EnableTool(self.wx_ids['Forward'], can_forward)

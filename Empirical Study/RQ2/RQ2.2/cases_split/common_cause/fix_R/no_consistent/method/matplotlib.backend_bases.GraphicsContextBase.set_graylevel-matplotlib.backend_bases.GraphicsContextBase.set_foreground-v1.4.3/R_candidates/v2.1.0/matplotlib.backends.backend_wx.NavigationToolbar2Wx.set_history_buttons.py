    def set_history_buttons(self):
        can_backward = (self._views._pos > 0)
        can_forward = (self._views._pos < len(self._views._elements) - 1)
        self.EnableTool(self.wx_ids['Back'], can_backward)
        self.EnableTool(self.wx_ids['Forward'], can_forward)

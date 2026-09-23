    def set_message(self, s):
        if self._coordinates:
            self._label_text.SetLabel(s)

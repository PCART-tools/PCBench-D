    def _keypress(self, event):
        if self.ignore(event):
            return
        if self.capturekeystrokes:
            key = event.key

            if len(key) == 1:
                self.text = (self.text[:self.cursor_index] + key +
                             self.text[self.cursor_index:])
                self.cursor_index += 1
            elif key == "right":
                if self.cursor_index != len(self.text):
                    self.cursor_index += 1
            elif key == "left":
                if self.cursor_index != 0:
                    self.cursor_index -= 1
            elif key == "home":
                self.cursor_index = 0
            elif key == "end":
                self.cursor_index = len(self.text)
            elif key == "backspace":
                if self.cursor_index != 0:
                    self.text = (self.text[:self.cursor_index - 1] +
                                 self.text[self.cursor_index:])
                    self.cursor_index -= 1
            elif key == "delete":
                if self.cursor_index != len(self.text):
                    self.text = (self.text[:self.cursor_index] +
                                 self.text[self.cursor_index + 1:])

            self.text_disp.remove()
            self.text_disp = self._make_text_disp(self.text)
            self._rendercursor()
            self._notify_change_observers()
            if key == "enter":
                self._notify_submit_observers()

    def set_message(self, s):
        self._message.emit(s)
        if self.coordinates:
            self.locLabel.setText(s)

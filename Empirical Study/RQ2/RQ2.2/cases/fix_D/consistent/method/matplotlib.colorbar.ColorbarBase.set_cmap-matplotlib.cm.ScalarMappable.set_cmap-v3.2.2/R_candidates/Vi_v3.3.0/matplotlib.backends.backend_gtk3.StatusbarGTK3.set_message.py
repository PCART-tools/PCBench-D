    def set_message(self, s):
        self.pop(self._context)
        self.push(self._context, s)

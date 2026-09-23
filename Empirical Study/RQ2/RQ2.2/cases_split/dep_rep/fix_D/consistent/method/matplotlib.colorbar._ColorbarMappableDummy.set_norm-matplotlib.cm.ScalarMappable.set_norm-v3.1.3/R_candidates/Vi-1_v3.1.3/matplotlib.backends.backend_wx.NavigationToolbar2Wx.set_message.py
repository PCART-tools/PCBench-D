    def set_message(self, s):
        if self.statbar is not None:
            self.statbar.set_function(s)

    def trigger(self, sender, event, data=None):
        """Calls `enable` or `disable` based on `toggled` value"""
        if self._toggled:
            self.disable(event)
        else:
            self.enable(event)
        self._toggled = not self._toggled

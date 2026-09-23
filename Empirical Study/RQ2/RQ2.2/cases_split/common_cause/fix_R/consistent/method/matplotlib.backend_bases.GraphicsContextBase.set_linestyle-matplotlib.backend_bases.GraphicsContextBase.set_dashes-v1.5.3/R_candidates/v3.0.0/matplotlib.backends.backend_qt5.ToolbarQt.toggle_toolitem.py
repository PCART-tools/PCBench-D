    def toggle_toolitem(self, name, toggled):
        if name not in self._toolitems:
            return
        for button, handler in self._toolitems[name]:
            button.toggled.disconnect(handler)
            button.setChecked(toggled)
            button.toggled.connect(handler)
